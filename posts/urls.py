from django.urls import path, include
from rest_framework import routers

from posts.views import (
    CommentsViewSet,
    PostsViewSet,
    # PostListCreateAPIView,
    # PostDetailAPIView,
)

router = routers.DefaultRouter()
posts_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
posts_router.register(r"comments", CommentsViewSet, basename="post-comments")

router.register("", PostsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:post_id>/comments/",
        CommentsViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="comments",
    ),
]

app_name = "posts"
