from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from user_profile.models import UserProfile
from user_profile.serializers import (
    UserProfileListSerializer,
    UserProfileDetailSerializer,
    UserProfileCreateSerializer,
)


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.select_related("user").prefetch_related(
        "followers", "following", "posts"
    )
    serializer_class = UserProfileListSerializer
    permission_classes = (IsAuthenticated | permissions.IsAdminUser,)

    def get_queryset(self):
        user = self.request.query_params.get("user")
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if user:
            queryset = queryset.filter(user__email__icontains=user)

        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=str,
                description="Search user by email (ex. ?user=user@test.com)",
            ),
            OpenApiParameter(
                name="username",
                type=str,
                description="Search user by username  (ex: ?username=Bob)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.select_related("user")
    serializer_class = UserProfileCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.select_related("user").prefetch_related(
        "followers", "following", "posts"
    )
    serializer_class = UserProfileDetailSerializer
    permission_classes = (IsAuthenticated | permissions.IsAdminUser,)


class UserProfileUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.select_related("user").prefetch_related(
        "followers", "following"
    )
    serializer_class = UserProfileDetailSerializer
    permission_classes = (IsAuthenticated | permissions.IsAdminUser,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes(
    IsAuthenticated,
)
def add_follower(request, pk, *args, **kwargs):
    current_profile = UserProfile.objects.get(user=request.user)
    current_user = request.user
    other_profile = UserProfile.objects.get(pk=pk)
    other_user = other_profile.user
    if current_user == other_user:
        raise ValueError("You can not follow yourself")
    other_profile.followers.add(current_user)
    current_profile.following.add(other_user)
    return redirect("user_profile:userprofile-detail", pk=other_profile.pk)


@api_view(["POST"])
@permission_classes(
    IsAuthenticated,
)
def remove_follower(request, pk, *args, **kwargs):
    current_profile = UserProfile.objects.get(user=request.user)
    current_user = request.user
    other_profile = UserProfile.objects.get(pk=pk)
    other_user = other_profile.user
    other_profile.followers.remove(current_user)
    current_profile.following.remove(other_user)
    return redirect("user_profile:userprofile-detail", pk=other_profile.pk)
