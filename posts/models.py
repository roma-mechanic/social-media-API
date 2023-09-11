import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api import settings


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class Post(models.Model):
    title = models.CharField(max_length=63)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=movie_image_file_path)
    likes = models.IntegerField(default=0, null=False)
    edited = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"Post id = {self.id}, author = {self.author}"

    def get_comments_count(self):
        return self.comments.all().count()


class Comments(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
