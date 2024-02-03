from rest_framework import serializers
from .models import Author, Media, Post

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    author = AuthorSerializer()
    class Meta:
        model = Post
        fields = '__all__'