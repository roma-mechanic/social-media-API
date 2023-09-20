from rest_framework import serializers

from user.models import User
from user_profile.models import UserProfile
from user.serializers import (
    UserListSerializer,
    UserSerializer,
    UserDetailSerializer,
)


class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserDetailSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "bio", "profile_image", "followers")


class UserProfileListSerializer(serializers.ModelSerializer):
    # user = UserDetailSerializer(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "followers",
        )
