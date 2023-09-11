from django.urls import path, include
from rest_framework import routers

from posts.views import CommentsViewSet, PostListCreateAPIView, PostDetailAPIView

router = routers.DefaultRouter()
router.register("", CommentsViewSet)

urlpatterns = [
    path("comments", include(router.urls)),
    path("", PostListCreateAPIView.as_view(), name="posts_list"),
    path("<int:pk>/", PostDetailAPIView.as_view(), name="post_detail")
]

app_name = "posts"
