from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.generics import (
    ListAPIView,
)

from permissions import IsAuthorOrReadOnly, IsAdminOrIfAuthenticatedReadOnly
from posts.mixin import LikedMixin
from posts.models import Comments, Post
from posts.serializers import (
    CommentSerializer,
    PostDetailSerializer,
    PostListSerializer,
    CommentDetailSerializer,
)
from user_profile.models import UserProfile


class PostReadOnlyViewSet(viewsets.ReadOnlyModelViewSet, LikedMixin):
    """
    Lists all the posts . Anon users can read post.

    EXAMPLE:
        GET -> /posts/ -> returns all posts
        GET -> /posts/{id}/ -> return the post detail
    """

    queryset = Post.objects.select_related("author").prefetch_related(
        "comments", "likes", "likes__user"
    )

    serializer_class = PostListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer




class PostCreateView(generics.CreateAPIView):
    """
    Create  new post. Must
    be logged in to create a post.

    EXAMPLE:
        POST -> /post/create/-> create new post
    """

    queryset = Post.objects.select_related("author")
    serializer_class = PostDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(
            author=UserProfile.objects.get(user=self.request.user)
        )


class PostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows user to delete their post. ID for the post required.
    Users can only delete their own posts. Also enable the retrieval
        of a single post details.

        GET -> /posts/<id>/ -> return the post detail with the post ID
        PUT, PATCH, DELETE -> /posts/<id>/update/ -> put, patch, delete post with post ID

    """

    queryset = Post.objects.select_related("author")
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(
            author=UserProfile.objects.get(user=self.request.user)
        )


class CommentsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet, LikedMixin):
    """
    Lists all the comments for a given post. Anon users can read comments. Must
    be logged in to create comments on the post, add/remove like.

    EXAMPLE:
        GET -> /posts/<post_id>/comments/ -> returns all comments for post with id
        GET -> /posts/<post_id>/comments/<comment_id>/ -> comment details
        POST -> /posts/<post_id>/comment/create/ -> create new comment on post with id
        POST -> /posts/<post_id>/comments/<comment_id>/like/ -> add like to this comment
        POST -> /posts/<post_id>/comments/<comment_id>/unlike/ -> remove like from this comment

        PLEASE NOTE: the word “comment” is spelled differently in different endpoints ("comment" and "comments")
    """

    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return (
            Comments.objects.filter(post__id=self.kwargs["post_pk"])
            .select_related("post", "author")
            .prefetch_related("likes")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CommentDetailSerializer
        return CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comments.objects.filter(
            post__id=self.kwargs["post_pk"]
        ).select_related("author", "post")

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        return serializer.save(
            author=UserProfile.objects.get(user=self.request.user), post=post
        )


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
     Allows user to delete, update their comment on a post. ID for the post and comment
     required. Users can only delete their own comments. Also enable the retrieval
     of a single comments details.

    EXAMPLE:
        GET -> /posts/<post_id>/comments/<comment_id>/ -> comment details
        PUT, PATCH, DELETE -> /posts/<post_id>/comments/<comment_id>/update/ -> update, delete comment

         PLEASE NOTE: the word “comment” is spelled differently in different endpoints ("comment" and "comments")
    """

    queryset = Comments.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAdminUser,
    )

    def get_queryset(self):
        return (
            Comments.objects.filter(post__id=self.kwargs["post_pk"])
            .select_related("post", "author")
            .prefetch_related("likes", "likes__user")
        )

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        return serializer.save(author=self.request.user, post=post)


class UserPostListAPIView(ListAPIView):
    """ """

    serializer_class = PostListSerializer

    def get_queryset(self):
        return (
            Post.objects.filter(author__id=self.kwargs["pk"])
            .select_related("author")
            .prefetch_related("comments", "likes")
        )
