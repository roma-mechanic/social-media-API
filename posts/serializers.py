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
        fields = ["id", "content", "created_at", "post", "author"]
        read_only_fields = ["date_created", "id"]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Post model. This serializer
    summarises the comments and author models.
    """

    # author = serializers.CharField(source="author")
    comments = serializers.IntegerField(
        source="get_comments_count", read_only=True
    )

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
            "edited",
        ]
        read_only_fields = ["id", "author", "date_created", "likes", "edited"]
