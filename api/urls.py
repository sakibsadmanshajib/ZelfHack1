from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import trigger_daily_task, PostListView

# router = DefaultRouter()
# router.register(r"posts", PostViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("trigger-daily-task/", trigger_daily_task),
]