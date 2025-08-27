from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import (
        Department,
        AffectedArea,
        Cause,
        ReportingLimitArea,
        LossOfProduction,
    )

    # Define models for different permission levels
    all_models = [Department, AffectedArea, Cause, ReportingLimitArea, LossOfProduction]
    lookup_models = [Department, AffectedArea, Cause, ReportingLimitArea]

    # Clear existing group permissions to ensure clean state
    Group.objects.filter(name__in=['Admin', 'Editor', 'Reader']).delete()

    # ADMIN GROUP - Full permissions on all models
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    for model in all_models:
        ct = ContentType.objects.get_for_model(model)
        # Add all permissions (add, change, delete, view)
        for action in ["add", "change", "delete", "view"]:
            try:
                perm = Permission.objects.get(
                    content_type=ct,
                    codename=f"{action}_{model._meta.model_name}"
                )
                admin_group.permissions.add(perm)
            except Permission.DoesNotExist:
                pass

    # EDITOR GROUP - Full permissions on LossOfProduction, view only on others
    editor_group, _ = Group.objects.get_or_create(name="Editor")

    # Full permissions on LossOfProduction
    ct = ContentType.objects.get_for_model(LossOfProduction)
    for action in ["add", "change", "delete", "view"]:
        try:
            perm = Permission.objects.get(
                content_type=ct,
                codename=f"{action}_lossofproduction"
            )
            editor_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass

    # View only permissions on lookup models
    for model in lookup_models:
        ct = ContentType.objects.get_for_model(model)
        try:
            perm = Permission.objects.get(
                content_type=ct,
                codename=f"view_{model._meta.model_name}"
            )
            editor_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass

    # READER GROUP - View only permissions on all models
    reader_group, _ = Group.objects.get_or_create(name="Reader")
    for model in all_models:
        ct = ContentType.objects.get_for_model(model)
        try:
            perm = Permission.objects.get(
                content_type=ct,
                codename=f"view_{model._meta.model_name}"
            )
            reader_group.permissions.add(perm)
        except Permission.DoesNotExist:
            pass


class LossofproductionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lossofproduction"

    def ready(self):
        post_migrate.connect(create_groups, sender=self)