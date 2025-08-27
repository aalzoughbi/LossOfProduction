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

    admin_models = [
        Department,
        AffectedArea,
        Cause,
        ReportingLimitArea,
        LossOfProduction,
    ]
    editor_models_view = [
        Department,
        AffectedArea,
        Cause,
        ReportingLimitArea,
        LossOfProduction,
    ]

    # Admin group - add & view on all models
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    for model in admin_models:
        ct = ContentType.objects.get_for_model(model)
        for action in ["add", "view"]:
            perms = Permission.objects.filter(content_type=ct, codename__startswith=f"{action}_")
            admin_group.permissions.add(*perms)

    # Editor group - add loss, view all
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    ct = ContentType.objects.get_for_model(LossOfProduction)
    editor_group.permissions.add(
        *Permission.objects.filter(content_type=ct, codename__startswith="add_")
    )
    for model in editor_models_view:
        ct = ContentType.objects.get_for_model(model)
        perm = Permission.objects.get(content_type=ct, codename=f"view_{model._meta.model_name}")
        editor_group.permissions.add(perm)

    # Reader group - view loss only
    reader_group, _ = Group.objects.get_or_create(name="Reader")
    ct = ContentType.objects.get_for_model(LossOfProduction)
    reader_group.permissions.add(
        Permission.objects.get(content_type=ct, codename="view_lossofproduction")
    )


class LossofproductionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lossofproduction"

    def ready(self):
        post_migrate.connect(create_groups, sender=self)
