from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from rest_framework import generics
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated

from user_profile.models import UserProfile
from user_profile.serializers import (
    UserProfileListSerializer,
    UserProfileDetailSerializer,
    UserProfileCreateSerializer,
)


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAuthenticated]


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]


class UserProfileUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
def add_follower(request, pk, *args, **kwargs):
    profile = UserProfile.objects.get(pk=pk)
    print(request.data)
    profile.followers.add(request.user)
    return redirect("user_profile:userprofile-detail", pk=profile.pk)


@api_view(["POST"])
def remove_follower(request, pk, *args, **kwargs):
    profile = UserProfile.objects.get(pk=pk)
    print(request.data)
    profile.followers.remove(request.user)
    return redirect("user_profile:userprofile-detail", pk=profile.pk)
