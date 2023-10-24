from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Post
from posts.serializers import PostListSerializer
from user.models import User
from user.serializers import (
    UserSerializer,
    UserDetailSerializer,
)

"""register user"""


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


"""Detail info by user"""


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                {"status": "OK, goodbye, all refresh tokens blacklisted"}
            )
        refresh_token = self.request.data.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


class UserPostListAPIView(ListAPIView):
    """Search for all posts by a given author by his UserProfile ID"""

    serializer_class = PostListSerializer

    def get_queryset(self):
        return (
            Post.objects.filter(author__id=self.kwargs["pk"])
            .select_related("author")
            .prefetch_related("comments", "likes")
        )
