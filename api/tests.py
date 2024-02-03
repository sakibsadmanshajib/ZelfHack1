from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Author, Post, Media  # Import your models here

class APIIntegrationTest(TestCase):
    def setUp(self):
        # Setup test data
        self.client = APIClient()
        self.author = Author.objects.create(name="Test Author", followers=1000, username="testauthor")
        self.post = Post.objects.create(creator=self.author, title="Test Post")
        Media.objects.create(post=self.post, url="http://example.com/image.jpg", media_type="IMAGE")
        
        # Endpoint URLs
        self.posts_url = reverse('api:posts-list', kwargs={'page_no': 1})  # Adjust based on your URL conf
        self.trigger_task_url = reverse('api:trigger-daily-task')
