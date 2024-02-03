# Generated by Django 5.0.1 on 2024-02-03 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("unique_id", models.IntegerField(primary_key=True, serialize=False)),
                ("unique_uuid", models.CharField(max_length=255)),
                ("origin_unique_id", models.CharField(max_length=255)),
                ("info_name", models.CharField(max_length=255)),
                ("info_platform", models.CharField(max_length=255)),
                ("username", models.CharField(max_length=255)),
                ("stats_followers_count", models.BigIntegerField()),
                ("avatar", models.URLField()),
                ("texts_profile", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("urls", models.URLField()),
                ("media_type", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("unique_id", models.IntegerField(primary_key=True, serialize=False)),
                ("unique_uuid", models.CharField(max_length=255)),
                ("origin_unique_id", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField()),
                ("main_text", models.TextField()),
                ("token_count", models.IntegerField()),
                ("char_count", models.IntegerField()),
                ("tag_count", models.IntegerField()),
                ("origin_platform", models.CharField(max_length=255)),
                ("origin_url", models.URLField()),
                ("stats_likes_count", models.BigIntegerField()),
                ("stats_views_count", models.BigIntegerField()),
                ("stats_comments_count", models.BigIntegerField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.author"
                    ),
                ),
                ("media", models.ManyToManyField(related_name="posts", to="api.media")),
            ],
        ),
    ]