from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts import services as likes_services
from posts.models import Comments, Post

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """

    author = serializers.CharField(source="author.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comments
        fields = [
            "id",
            "content",
            "created_at",
            "post",
            "author",
            "total_likes",
        ]
        read_only_fields = ["date_created", "id"]


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)
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


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Post model. This serializer
    summarises the comments and author models.
    """

    comments = serializers.IntegerField(
        source="get_comments_count", read_only=True
    )
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "comments",
            "date_created",
            "total_likes",
        ]
        read_only_fields = [
            "id",
            "author",
            "date_created",
            "total_likes",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField(
        source="get_comments_count", read_only=True
    )
    author = serializers.CharField(source="author.username", read_only=True)
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
        ]
        read_only_fields = [
            "id",
            "author",
            "date_created",
            "total_likes",
        ]

    def get_is_fan(self, obj) -> bool:
        """
        Checks if `request.user` liked the post (`obj`).
        """
        user = self.context.get("request").user
        likes_users = obj.likes.values_list("user_id", flat=True)
        return user.id in likes_users
