from rest_framework import serializers

from posts.models import Comments, Post
from user.serializers import UserListSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """

    author = UserListSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field="id", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "text", "date_created", "post", "author"]
        read_only_fields = ["date_created", "id"]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Post model. This serializer
    summarises the comments and author models.
    """

    author = serializers.ReadOnlyField(source="author.username")
    comments = serializers.IntegerField(
        source="get_comments_count", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "text",
            "author",
            "likes",
            "comments",
            "date_created",
            "edited",
        ]
        read_only_fields = ["uuid", "author", "date_created", "pins", "edited"]
