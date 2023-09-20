import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api import settings


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.info)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(
        upload_to=movie_image_file_path, blank=True
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_followers", blank=True
    )
