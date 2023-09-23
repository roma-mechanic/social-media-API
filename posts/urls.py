from django.urls import path, include
from rest_framework_nested import routers

from posts.views import (
    PostsViewSet,
    CommentsReadOnlyViewSet,
    CommentCreateView,
    CommentUpdateView,
)

router = routers.SimpleRouter()
router.register(r"posts", PostsViewSet)

comments_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
comments_router.register(
    r"comments", CommentsReadOnlyViewSet, basename="post-comments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comments_router.urls)),
    path(
        "posts/<int:post_pk>/comment/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "posts/<int:post_pk>/comment/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
]

app_name = "posts"
