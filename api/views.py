from rest_framework.generics import ListAPIView
from .models import Post
from .serializers import PostSerializer
from .pagination import CustomPagination
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from .tasks import daily_update_posts
from django.conf import settings

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination

@require_http_methods(["POST"])  # Restrict this view to POST requests
def trigger_daily_task(request):
    # Retrieve the secret key sent in the request
    # Example using a custom header 'X-Secret-Key'
    secret_key = request.headers.get('X-API-KEY')
    expected_key = settings.X_API_KEY
    
    # Compare the provided secret key with the expected one
    if secret_key == expected_key:
        # If keys match, trigger the Celery task
        daily_update_posts.delay()
        # daily_update_posts.s().apply_async().get()
        return JsonResponse({'status': 'Task triggered successfully'})
    else:
        # If keys do not match, return a forbidden response
        return HttpResponseForbidden({'status': 'Invalid API key'})
