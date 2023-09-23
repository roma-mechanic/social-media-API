from django.urls import path

from posts.views import UserPostListAPIView
from user_profile.views import (
    UserProfileListView,
    UserProfileCreateView,
    UserProfileDetailView,
    UserProfileUpdateDeleteView,
)

urlpatterns = [
    path("", UserProfileListView.as_view(), name="userprofile-list"),
    path(
        "create/", UserProfileCreateView.as_view(), name="userprofile-create"
    ),
    path(
        "<int:pk>/", UserProfileDetailView.as_view(), name="userprofile-detail"
    ),
    path(
        "<int:pk>/update/",
        UserProfileUpdateDeleteView.as_view(),
        name="userprofile-update",
    ),
    path("<int:pk>/posts/", UserPostListAPIView.as_view(), name="user-posts"),
]

app_name = "user_profile"
