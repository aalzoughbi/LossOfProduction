from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import *


class PermissionControlMixin:
    """
    Mixin to control admin permissions based on user groups
    """

    def has_module_permission(self, request):
        """Control whether the module appears in admin"""
        if request.user.is_superuser:
            return True

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # All three groups should see these modules in admin
        if {'Admin', 'Editor', 'Reader'} & user_groups:
            return True

        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        """Control view permission"""
        if request.user.is_superuser:
            return True

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # All groups have view permission
        if {'Admin', 'Editor', 'Reader'} & user_groups:
            return True

        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        """Control add permission"""
        if request.user.is_superuser:
            return True

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # Check if this is a lookup model or LossOfProduction
        model_name = self.model._meta.model_name

        if model_name == 'lossofproduction':
            # Admin and Editor can add LossOfProduction
            return bool({'Admin', 'Editor'} & user_groups)
        else:
            # Only Admin can add lookup models
            return 'Admin' in user_groups

        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        """Control change permission"""
        if request.user.is_superuser:
            return True

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # Check if this is a lookup model or LossOfProduction
        model_name = self.model._meta.model_name

        if model_name == 'lossofproduction':
            # Admin and Editor can change LossOfProduction
            return bool({'Admin', 'Editor'} & user_groups)
        else:
            # Only Admin can change lookup models
            return 'Admin' in user_groups

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Control delete permission"""
        if request.user.is_superuser:
            return True

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # Check if this is a lookup model or LossOfProduction
        model_name = self.model._meta.model_name

        if model_name == 'lossofproduction':
            # Admin and Editor can delete LossOfProduction
            return bool({'Admin', 'Editor'} & user_groups)
        else:
            # Only Admin can delete lookup models
            return 'Admin' in user_groups

        return super().has_delete_permission(request, obj)


@admin.register(Department)
class DepartmentAdmin(PermissionControlMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AffectedArea)
class AffectedAreaAdmin(PermissionControlMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Cause)
class CauseAdmin(PermissionControlMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ReportingLimitArea)
class ReportingLimitAreaAdmin(PermissionControlMixin, admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')
    autocomplete_fields = ('department',)


@admin.register(LossOfProduction)
class LossOfProductionAdmin(PermissionControlMixin, admin.ModelAdmin):
    list_display = ('id', 'issue_date', 'department', 'affected_area', 'event_type', 'status', 'date_solved',)
    list_filter = ('department', 'affected_area', 'event_type', 'status', 'cause',)
    search_fields = ('id', 'equipment_or_process_step', 'description', 'reporting_limit',)
    autocomplete_fields = ('department', 'affected_area', 'cause', 'reporting_limit_area',)

    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly for Reader group"""
        if request.user.is_superuser:
            return ()

        user_groups = set(request.user.groups.values_list('name', flat=True))

        # Reader group gets readonly fields
        if 'Reader' in user_groups and not ({'Admin', 'Editor'} & user_groups):
            return [f.name for f in self.model._meta.fields]

        return super().get_readonly_fields(request, obj)