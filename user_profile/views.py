from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdminOrIfAuthenticatedReadOnly
from user.serializers import UserListSerializer, UserSerializer
from user_profile.models import UserProfile
from user_profile.serializers import (
    UserProfileSerializer,
    UserProfileListSerializer,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.prefetch_related("user", "followers")
    serializer_class = UserProfileSerializer
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return UserProfileListSerializer
        return UserProfileSerializer
