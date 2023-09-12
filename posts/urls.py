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
# router.register("/<int:id>/comments/", CommentsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("post-list/", PostListCreateAPIView.as_view(), name="posts_list"),
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
