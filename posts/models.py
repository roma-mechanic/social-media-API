import os
import uuid

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from social_media_api import settings
from user.models import UserProfile


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/post", filename)


class Post(models.Model):
    title = models.CharField(max_length=63)
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=movie_image_file_path)
    likes = GenericRelation(Like, default=0)
    is_publish = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"Post id = {self.id}, author = {self.author}"

    def total_likes(self) -> int:
        return self.likes.count()

    def get_comments_count(self) -> int:
        return self.comments.count()


class Comments(models.Model):
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like, default=0)

    class Meta:
        ordering = ["-created_at"]

    def total_likes(self) -> int:
        return self.likes.count()
