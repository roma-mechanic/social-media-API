from rest_framework import serializers

from user.models import User
from user_profile.models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "username",
            "bio",
            "profile_image",
        )


class UserProfileDetailSerializer(serializers.ModelSerializer):
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
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "followers",
        )
        read_only_fields = ("followers",)


class UserProfileListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "username",
            "profile_image",
            "followers",
            "following",
        )


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
        )

    def get_full_name(self, obj):
        return obj.get_full_name()
