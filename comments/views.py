from django.shortcuts import render
from rest_framework import viewsets

from comments.models import Comments
from comments.serializers import CommentSerializer
from permissions import IsAdminOrIfAuthenticatedReadOnly


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.prefetch_related("user", "post")
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
