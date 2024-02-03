from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Post
from .serializers import PostSerializer

class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer