from django.urls import path, include
from rest_framework import routers

from posts.views import (
    CommentsViewSet,
    PostsViewSet,
    # PostListCreateAPIView,
    # PostDetailAPIView,
)

router = routers.DefaultRouter()
router.register("", PostsViewSet)
router.register("comments/", CommentsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("post-list/", PostListCreateAPIView.as_view(), name="posts_list"),
    # path("post/<int:pk>/", PostDetailAPIView.as_view(), name="post_detail"),
]

app_name = "posts"
