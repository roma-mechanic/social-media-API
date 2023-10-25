from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(UserSerializer):
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = ("id", "email", "full_name")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "first_name",
            "last_name",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


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
    followers = serializers.SlugRelatedField(
        slug_field="email", many=True, read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field="email", many=True, read_only=True
    )

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
            "following",
        )
        read_only_fields = ("followers", "following")


class UserProfileListSerializer(serializers.ModelSerializer):
    count_posts = serializers.IntegerField(source="get_posts_count")

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user_id",
            "username",
            "count_posts",
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
