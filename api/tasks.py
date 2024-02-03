from celery import shared_task
from celery.utils.log import get_task_logger
import requests
from .models import Author, Post, Media
from django.conf import settings

logger = get_task_logger(__name__)

API_BASE_URL = settings.API_BASE_URL

headers = {
    'X-API-Key': settings.X_API_KEY
}

@shared_task(bind=True, default_retry_delay=0, max_retries=3, rate_limit='10/m')
def fetch_and_prepare_author_data(self, unique_id):
    url = f"{API_BASE_URL}/authors/{unique_id}"
    try:
        response = requests.get(url, headers=headers)
        
        # Directly raise for status to catch all 4xx and 5xx errors.
        response.raise_for_status()

        data = response.json().get('data', [])
        if not data:
            logger.info(f"No data found for unique_id: {unique_id}")
            return None

        author_data = data[0]
        prepared_data = {
            'unique_id': author_data['unique_id'],
            'unique_uuid': author_data['unique_uuid'],
            'origin_unique_id': author_data['origin_unique_id'],
            'info_name': author_data['info']['name'],
            'info_platform': author_data['info']['platform'],
            'username': author_data['username'],
            'stats_followers_count': int(author_data['stats']['digg_count']['followers']['count']),
            'avatar': author_data['avatar']['urls'][0],
            'texts_profile': author_data['texts']['profile_text'],
        }

        return prepared_data
    except requests.exceptions.HTTPError as http_err:
        # For 5xx server errors and 400 Bad Request, retry the task
        if 500 <= response.status_code < 600 or response.status_code == 400:
            logger.error(f"Retryable error {response.status_code}: {http_err}. Retrying...")
            raise self.retry(exc=http_err)
        elif response.status_code == 404:
            logger.info(f"Author with unique_id {unique_id} not found. Not retrying.")
            return {'error': 'Not found'}
        else:
            logger.error(f"HTTP error {response.status_code}: {http_err}")
            return {'error': f'HTTP error: {response.status_code}'}
    except requests.RequestException as req_err:
        logger.error(f"Request failed: {req_err} - URL: {url}")
        # Retry for other types of request exceptions
        raise self.retry(exc=req_err)
    except Exception as exc:
        logger.error(f"Unexpected error for unique_id {unique_id}: {exc}")
        # Retry for unexpected errors
        raise self.retry(exc=exc)


@shared_task(bind=True, default_retry_delay=0, max_retries=3, rate_limit='2/m')
def fetch_contents(self, page_no):
    url = f"{API_BASE_URL}/contents?page={page_no}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        prepared_data = []
        for item in data['data']:
            post_data = {
                "unique_id": item['unique_id'],
                "unique_uuid": item['unique_uuid'],
                "origin_unique_id": item['origin_unique_id'],
                "created_at": item['creation_info']['created_at'],
                "author_id": item['author']['id'],
                "main_text": item['context']['main_text'],
                "token_count": item['context']['token_count'],
                "char_count": item['context']['char_count'],
                "tag_count": item['context']['tag_count'],
                "origin_platform": item['origin_details']['origin_platform'],
                "origin_url": item['origin_details']['origin_url'],
                "stats_likes_count": item['stats']['digg_counts']['likes']['count'],
                "stats_views_count": item['stats']['digg_counts']['views']['count'],
                "stats_comments_count": item['stats']['digg_counts']['comments']['count'],
                "media": [
                    {"urls": media_url, "media_type": item['media']['media_type']}
                    for media_url in item['media']['urls']
                ],
            }
            prepared_data.append(post_data)

        # Here you could write prepared_data to a JSON file, or directly create models
        return prepared_data, data['next']
    except requests.exceptions.HTTPError as http_err:
        # For 5xx server errors and 400 Bad Request, retry the task
        if 500 <= response.status_code < 600 or response.status_code == 400:
            logger.error(f"Retryable error {response.status_code}: {http_err}. Retrying...")
            raise self.retry(exc=http_err)
        elif response.status_code == 404:
            logger.info(f"Page {page_no} not found. Not retrying.")
            return {'error': 'Not found'}
        else:
            logger.error(f"HTTP error {response.status_code}: {http_err}")
            return {'error': f'HTTP error: {response.status_code}'}
    except requests.RequestException as req_err:
        logger.error(f"Request failed: {req_err} - URL: {url}")
        # Retry for other types of request exceptions
        raise self.retry(exc=req_err)
    except Exception as exc:
        logger.error(f"Unexpected error for page {page_no}: {exc}")
        # Retry for unexpected errors
        raise self.retry(exc=exc)

@shared_task
def daily_update_posts(page_no=1):
    while True:
        post_data, next = fetch_contents.s(page_no).apply_async().get()
        
        if post_data is None or 'error' in post_data:
            logger.error(f"Error fetching page {page_no}. Stopping...")
            break
        logger.info(f"Processing page {page_no} with {len(post_data)} items")
        for item in post_data:
            # Check and add/update author
            author_id = item['author_id']
            if not Author.objects.filter(unique_id=author_id).exists():
                author_data = fetch_and_prepare_author_data.s(author_id).apply_async().get()
                if author_data and 'error' not in author_data:
                    Author.objects.create(**author_data)
            logger.info(f"Processing post {item['unique_id']}")
            # Check if post exists
            if not Post.objects.filter(unique_id=item['unique_id']).exists():
                # Process and add media
                new_media = []
                for media in item['media']:
                    new_media.append(Media.objects.create(**media))
                # Create new post
                new_post = Post.objects.create(
                    unique_id=item['unique_id'],
                    unique_uuid=item['unique_uuid'],
                    origin_unique_id=item['origin_unique_id'],
                    created_at=item['created_at'],
                    author=Author.objects.get(unique_id=author_id),
                    main_text=item['main_text'],
                    token_count=item['token_count'],
                    char_count=item['char_count'],
                    tag_count=item['tag_count'],
                    origin_platform=item['origin_platform'],
                    origin_url=item['origin_url'],
                    stats_likes_count=item['stats_likes_count'],
                    stats_views_count=item['stats_views_count'],
                    stats_comments_count=item['stats_comments_count']
                )
                new_post.media.set(new_media)
                new_post.save()
            else:
                logger.info(f"Post {item['unique_id']} already exists. Skipping...")
        logger.info(f"Page {page_no} processed successfully")
        if next is not isinstance(int):
            logger.info(f"Current Page {page_no} No more pages. Stopping...")
            break  # No more pages
        page_no = next
