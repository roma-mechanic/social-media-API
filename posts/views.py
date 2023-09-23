from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.generics import (
    ListAPIView,
)

from permissions import IsAuthorOrReadOnly
from posts.mixin import LikedMixin
from posts.models import Comments, Post
from posts.serializers import CommentSerializer, PostSerializer


class PostsViewSet(viewsets.ModelViewSet, LikedMixin):
    """
    Lists all the posts for a given user. Anon users can read post. Must
    be logged in to create a post.

    EXAMPLE:
        GET -> /posts/ -> returns all posts
        POST -> /posts/-> create new post

    Allows user to delete their post. ID for the post required.
    Users can only delete their own posts. Also enable the retrieval
        of a single post details.

        GET -> /posts/<id>/ -> return the post detail with the post ID
        PUT, PATCH, DELETE -> /posts/<id>/ -> put, patch, delete post with post ID

    """

    queryset = Post.objects.prefetch_related("author")
    serializer_class = PostSerializer

    # permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            author_id = self._params_to_ints(author)
            queryset = queryset.filter(author__id__in=author_id)
        return queryset.distinct()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


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

    queryset = Comments.objects.prefetch_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Comments.objects.filter(post__id=self.kwargs["post_pk"])


class CommentCreateView(generics.CreateAPIView):
    queryset = Comments.objects.prefetch_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comments.objects.filter(post__id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        return serializer.save(author=self.request.user, post=post)


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
     Allows user to delete, update their comment on a post. ID for the post and comment
     required. Users can only delete their own comments. Also enable the retrieval
     of a single comments details.

    EXAMPLE:
        GET -> /posts/<post_id>/comments/<comment_id>/ -> comment details
        PUT, PATCH, DELETE -> /posts/<post_id>/comment/<comment_id>/update/ -> update, delete comment

         PLEASE NOTE: the word “comment” is spelled differently in different endpoints ("comment" and "comments")
    """

    queryset = Comments.objects.prefetch_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, permissions.IsAdminUser)

    def get_queryset(self):
        return Comments.objects.filter(post__id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        return serializer.save(author=self.request.user, post=post)


class UserPostListAPIView(ListAPIView):
    """ """

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs["pk"])
