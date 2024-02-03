from rest_framework import serializers
from .models import Post, Author, Media

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='unique_id')
    followers = serializers.IntegerField(source='stats_followers_count')
    external_id = serializers.CharField(source='origin_unique_id')
    external_url = serializers.SerializerMethodField()
    name = serializers.CharField(source='info_name')
    email = serializers.SerializerMethodField()
    platform = serializers.CharField(source='info_platform')
    profile_text = serializers.CharField(source='texts_profile')
    profile_picture_url = serializers.URLField(source='avatar')
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'followers', 'username', 'external_id', 
                  'external_url', 'name', 'email', 'platform', 'profile_text', 
                  'profile_picture_url', 'follower_count')
        
    def get_external_url(self, obj):
        return ""
    
    def get_email(self, obj):
        return ""
    
    def get_follower_count(self, obj):
        return str(obj.stats_followers_count)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'urls', 'media_type')

class PostSerializer(serializers.ModelSerializer):
    creator = AuthorSerializer(source='author', many=False)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('creator', 'content')

    def get_content(self, obj):
        # Assuming these fields exist on the Post model; adjust as necessary
        return {
            'id': obj.unique_id,
            'uuid': obj.unique_uuid,
            'account': obj.author.unique_id,
            'external_id': obj.origin_unique_id,
            'external_url': obj.origin_url,
            'timestamp': obj.created_at,
            'title': obj.main_text,
            'text': obj.main_text,
            'thumbnail_url': obj.media.first().urls if obj.media.exists() else None,
            'content_platform': obj.origin_platform,
            'content_type': None,
            'content_form': obj.media.first().media_type if obj.media.exists() else None,
            'likes': obj.stats_likes_count,
            'comments': obj.stats_comments_count,
            'views': obj.stats_views_count,
            'shares': 0,
            'total_engagement': obj.stats_likes_count + obj.stats_comments_count,
            'engagement_of_views': (obj.stats_likes_count + obj.stats_comments_count) / obj.stats_views_count if obj.stats_views_count > 0 else 0,
            'engagement_of_followers': (obj.stats_likes_count + obj.stats_comments_count) / obj.author.stats_followers_count if obj.author.stats_followers_count > 0 else 0,
        }
