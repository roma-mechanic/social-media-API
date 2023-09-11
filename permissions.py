from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                    request.method in SAFE_METHODS
                    and request.user
                    and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)

        )


class IsAuthorOrReadOnly(BasePermission):
    """
    Checks that the authorised user is the owner of the resource when making non
    safe http requests.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
