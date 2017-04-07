from rest_framework.permissions import BasePermission


class IsParentCardOwner(BasePermission):
    """
    Checks if the user is assigned as parent to the card

    TODO: Use django object permissions instead

    http://www.django-rest-framework.org/api-guide/permissions/#djangoobjectpermissions
    """
    def has_object_permission(self, request, view, obj):
        return obj.parent == request.user
