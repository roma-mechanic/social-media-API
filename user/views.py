from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
)

"""register user"""


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


"""Detail info by user"""


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    # authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
