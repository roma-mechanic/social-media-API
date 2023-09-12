from django.urls import path, include
from rest_framework_nested import routers

from posts.views import (
    CommentsViewSet,
    PostsViewSet,
)

router = routers.SimpleRouter()
router.register(r"posts", PostsViewSet)

comments_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
comments_router.register(
    r"comments", CommentsViewSet, basename="post-comments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comments_router.urls)),
]

app_name = "posts"
