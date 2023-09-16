from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comments, Post
from user.serializers import UserListSerializer
from posts import services as likes_services

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """

    author = UserListSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field="id", read_only=True)
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = [
            "id",
            "content",
            "created_at",
            "post",
            "author",
            "is_fan",
            "total_likes",
        ]
        read_only_fields = ["date_created", "id"]

    def get_is_fan(self, obj) -> bool:
        """
        Checks if `request.user` liked the comments (`obj`).
        """
        user = self.context.get("request").user
        return likes_services.is_fan(obj, user)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Post model. This serializer
    summarises the comments and author models.
    """

    # author = serializers.CharField(source="author")
    comments = serializers.IntegerField(
        source="get_comments_count", read_only=True
    )
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "image",
            "comments",
            "date_created",
            "is_fan",
            "total_likes",
            "edited",
        ]
        read_only_fields = [
            "id",
            "author",
            "date_created",
            "total_likes",
            "edited",
        ]

    def get_is_fan(self, obj) -> bool:
        """
        Checks if `request.user` liked the post (`obj`).
        """
        user = self.context.get("request").user
        return likes_services.is_fan(obj, user)


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
