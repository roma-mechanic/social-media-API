import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from social_media_api import settings
from user.models import User

USER = get_user_model()


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/user", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    username = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(
        upload_to=movie_image_file_path, blank=True
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="follower",
        blank=True,
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="following", blank=True
    )

    def get_posts_count(self):
        return self.posts.count()
