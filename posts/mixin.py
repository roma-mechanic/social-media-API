from rest_framework.decorators import action
from rest_framework.response import Response
from posts import services
from .serializers import FanSerializer


class LikedMixin:

    def get_object(self):
        pass

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        """
        liked `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=["POST"])
    def unlike(self, request, pk=None):
        """
        Removes like from `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(methods=["GET"])
    def fans(self, request, pk=None):
        """
        Gets all users who liked `obj`
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
