# ZelfHack1 API Documentation

ZelfHack1 is a Django-based project utilizing an external RabbitMQ (CloudAMQP) instance as its message broker.

## Setup Process

1. **Install Python Virtual Environment (Python 3.10)**:
 - Create and activate a virtual environment to isolate the project dependencies.

2. **Clone Git Repository and Install Packages**:
 - Clone the repository and install the required packages using:
	```bash
     pip install -r requirements.txt
     ``` 
3. **Start Celery Worker**:
 - Start the Celery worker with debugging enabled and using the `gevent` pool:
	 ```bash
     celery -A ZelfHack1 worker -l debug -P gevent
     ``` 
4. **Database Migration and Django Server**:
 - Migrate the database and start the Django development server.
	  ```bash
	  python manage.py migrate
	  python manage.py runserver
	  ```
	  
5. **Run Endpoint 2**:
 - Trigger data parsing by making a request to Endpoint 2. Look at the celery debug windows for to finish parsing.

6. **Run Endpoint 1**:
 - Access paginated posts data through Endpoint 1.

## Endpoints

### Endpoint 1: Fetch Paginated Posts

- **URL**: `{url}/api/v1/posts/?page={page_no}`
- **Method**: GET
- **Response**:
  ```json
  {
      "page": 6,
      "next": null,
      "data": [
          {
              "creator": {
                  "id": 302048,
                  "followers": 931900,
                  "username": "sephora",
                  "external_id": "279484737629323264",
                  "external_url": "",
                  "name": "sephora",
                  "email": "",
                  "platform": "instagram",
                  "profile_text": "We belong to something beautiful.",
                  "profile_picture_url": "https://p16-sign-sg.tiktokcdn.com/aweme/1080x1080/tos-alisg-avt-0068/smg71630d66b7a573be2525c01e74f615fe.jpeg?x-expires=1678014000&x-signature=v0NHfB5gs46Cuhx4I1A0QOHdmjA%3D",
                  "follower_count": "931900"
              },
              "content": {
                  "id": 5516295,
                  "uuid": "e580355b-0583-4cff-ad20-13445673a306",
                  "account": 302048,
                  "external_id": "7293636110335348011",
                  "external_url": "https://tiktok.com/@sephora/video/7293636110335348011",
                  "timestamp": "2023-10-24T21:13:24Z",
                  "title": "@Sam Talu 🍒’s fiancé has exquisite taste in skincare. #SephoraSquad",
                  "text": "@Sam Talu 🍒’s fiancé has exquisite taste in skincare. #SephoraSquad",
                  "thumbnail_url": "https://nyc3.digitaloceanspaces.com/hellozelf/content/77b6b9b6-2572-44fd-af42-7bcd102e34e7.jpg",
                  "content_platform": "instagram",
                  "content_type": null,
                  "content_form": "VIDEO",
                  "likes": 35600,
                  "comments": 56,
                  "views": 10600000,
                  "shares": 0,
                  "total_engagement": 35656,
                  "engagement_of_views": 0.0033637735849056604,
                  "engagement_of_followers": 0.0382616160532246
              }
          },
          ....
      ],
      "total_contents": 158,
      "page_size": 30
  }`` 

### Endpoint 2: Trigger Data Parsing

-   **URL**: `{url}/api/v1/trigger-daily-task/`
-   **Method**: POST
-   **Header**:
    
    ```json
    {
      "X-API-KEY": "key"
    }
    ```
    
-   **Response**:
    ```json
    {
      "status": "Task triggered successfully"
    }
    ``` 
    

This endpoint is used for triggering data parsing and can be scheduled for automatic execution according to business requirements using Celery's scheduled tasks.


**
N.B.: Replace `{url}` with your actual server URL and `"key"` with the actual API key value required to authenticate the request to Endpoint.
**
