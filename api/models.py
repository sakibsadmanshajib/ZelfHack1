from django.db import models

class Author(models.Model):
    unique_id = models.IntegerField(primary_key=True)
    unique_uuid = models.CharField(max_length=255)
    origin_unique_id = models.CharField(max_length=255)
    info_name = models.CharField(max_length=255)
    info_platform = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    stats_followers_count = models.BigIntegerField()
    avatar = models.URLField()
    texts_profile = models.TextField()

class Media(models.Model):
    urls = models.URLField()
    media_type = models.CharField(max_length=255)

class Post(models.Model):
    unique_id = models.IntegerField(primary_key=True)
    unique_uuid = models.CharField(max_length=255)
    origin_unique_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    main_text = models.TextField()
    token_count = models.IntegerField()
    char_count = models.IntegerField()
    tag_count = models.IntegerField()
    origin_platform = models.CharField(max_length=255)
    origin_url = models.URLField()
    stats_likes_count = models.BigIntegerField()
    stats_views_count = models.BigIntegerField()
    stats_comments_count = models.BigIntegerField()
    media = models.ManyToManyField('Media', related_name='posts')

