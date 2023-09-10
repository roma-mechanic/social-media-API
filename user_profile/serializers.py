from rest_framework import serializers

from user_profile.models import UserProfile
from user.serializers import UserListSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer

    class Meta:
        model = UserProfile
        fields = ("id", "bio", "profile_image", "followers", "friends")
