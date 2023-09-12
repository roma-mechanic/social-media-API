from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdminOrIfAuthenticatedReadOnly, IsAuthorOrReadOnly
from posts.models import Comments, Post
from posts.serializers import CommentSerializer, PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("author")
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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
        serializer.save(author=self.request.user)


# class PostListCreateAPIView(ListCreateAPIView):
#     """
#     Lists the currently logged in users posts with a GET and allows a user to
#     create a new post with POST. Must be logged in to access this route.
#
#     EXAMPLE:
#         GET -> /posts/ -> return a list of posts
#         POST -> /posts/ -> create new post
#     """
#
#     queryset = Post.objects.prefetch_related("author")
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         """
#         Return all posts for logged in user.
#         """
#         return Post.objects.filter(author=self.request.user)
#
#     def perform_create(self, serializer):
#         return serializer.save(author=self.request.user)
#
#
# class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
#     """
#     Selects post by ID and displays it's details. Anon users able to read post
#     details with GET. Must be authenticated and be the owner of the post to make
#     PUT and DELETE requests.
#
#     EXAMPLE:
#         GET -> /posts/<id>/ -> return post details
#         PUT -> /posts/<id>/ -> make an edit to the post text (if owner)
#         DELETE -> /posts/<id>/ -> delete post (if owner)
#     """
#
#     queryset = Post.objects.prefetch_related("author")
#     lookup_field = "id"
#
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthorOrReadOnly]
#
#     def perform_update(self, serializer):
#         return serializer.save(edited=True)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Lists all the comments for a given post. Anon users can read comments. Must
    be logged in to create comments on the post.

    EXAMPLE:
        GET -> /posts/<id>/comments/ -> returns all comments for post with id
        POST -> /posts/<id>/comments/ -> create new comment on post with id
    """

    queryset = Comments.objects.prefetch_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Comments.objects.filter(post__id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs["post_pk"])
        return serializer.save(author=self.request.user, post=post)

    """
        Allows user to delete their comment on a post. ID for the post and comment
        required. Users can only delete their own comments. Also enable the retrieval
        of a single comments details.

        EXAMPLE:
            GET -> /posts/<post_id>/comments/<comment_id>/ -> comment details
            DELETE -> /posts/<post_id>/comments/<comment_id>/ -> delete comment
    """

    def get_object(self):
        comment = get_object_or_404(
            Comments,
            id=self.kwargs["pk"],
            post__id=self.kwargs["post_pk"],
        )
        self.check_object_permissions(self.request, comment)
        return comment


class UserPostListAPIView(ListAPIView):
    """ """

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs["id"])
