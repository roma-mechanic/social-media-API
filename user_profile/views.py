from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user_profile.models import UserProfile
from user_profile.serializers import (
    UserProfileListSerializer,
    UserProfileDetailSerializer,
)


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAuthenticated]


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileDetailSerializer
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
