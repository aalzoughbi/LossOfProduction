from rest_framework.permissions import BasePermission, DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """
    Enhanced DjangoModelPermissions that properly handles view permissions
    and provides granular control based on user groups.
    """

    # Include view permission in required permissions
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow superusers full access
        if request.user.is_superuser:
            return True

        return super().has_permission(request, view)


class LookupModelPermissions(CustomDjangoModelPermissions):
    """
    Permission class for lookup models (Department, AffectedArea, Cause, ReportingLimitArea).
    Admin: Full CRUD access
    Editor: Read-only access
    Reader: Read-only access
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user
        user_groups = set(user.groups.values_list('name', flat=True))

        # Admin group has full access
        if 'Admin' in user_groups:
            return True

        # Editor and Reader groups have read-only access
        if {'Editor', 'Reader'} & user_groups:
            return request.method in ['GET', 'HEAD', 'OPTIONS']

        # Fallback to standard Django model permissions
        return super().has_permission(request, view)


class LossOfProductionPermissions(CustomDjangoModelPermissions):
    """
    Permission class for LossOfProduction model.
    Admin: Full CRUD access
    Editor: Full CRUD access
    Reader: Read-only access
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user
        user_groups = set(user.groups.values_list('name', flat=True))

        # Admin and Editor groups have full access
        if {'Admin', 'Editor'} & user_groups:
            return True

        # Reader group has read-only access
        if 'Reader' in user_groups:
            return request.method in ['GET', 'HEAD', 'OPTIONS']

        # Fallback to standard Django model permissions
        return super().has_permission(request, view)