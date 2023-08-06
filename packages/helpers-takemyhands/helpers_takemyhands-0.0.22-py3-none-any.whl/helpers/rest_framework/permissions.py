from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    """ Is Owner Permission Definition """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSelf(BasePermission):

    """ Is Self Permission Definition """

    def has_object_permission(self, request, view, user):
        return bool(user == request.user)