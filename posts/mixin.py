from rest_framework.decorators import action
from rest_framework.response import Response
from posts import services
from user.serializers import UserListSerializer
from .serializers import FanSerializer


class LikedMixin:
    @action(detail=True, methods=["POST"])
    def like(self, request, **kwargs):
        """
        liked `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=["POST"])
    def unlike(self, request, **kwargs):
        """
        Removes like from `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=["GET"])
    def fans(self, request, **kwargs):
        """
        Gets all users who liked `obj`
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = UserListSerializer(fans, many=True)
        return Response(serializer.data)
