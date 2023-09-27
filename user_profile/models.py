import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api import settings


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
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
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

    # def count_followers(self):
    #     return self.followers.count()

    # def count_following(self):
    #     return User.objects.filter(followers=self).count()
