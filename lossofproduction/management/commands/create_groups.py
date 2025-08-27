# Save this as: lossofproduction/management/commands/create_groups.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from lossofproduction.models import (
    Department,
    AffectedArea,
    Cause,
    ReportingLimitArea,
    LossOfProduction,
)


class Command(BaseCommand):
    help = 'Create permission groups for the application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recreate',
            action='store_true',
            help='Delete existing groups and recreate them',
        )

    def handle(self, *args, **options):
        if options['recreate']:
            self.stdout.write('Deleting existing groups...')
            Group.objects.filter(name__in=['Admin', 'Editor', 'Reader']).delete()

        # Define models for different permission levels
        all_models = [Department, AffectedArea, Cause, ReportingLimitArea, LossOfProduction]
        lookup_models = [Department, AffectedArea, Cause, ReportingLimitArea]

        self.stdout.write('Creating permission groups...')

        # ADMIN GROUP - Full permissions on all models
        admin_group, created = Group.objects.get_or_create(name="Admin")
        if created:
            self.stdout.write(f'Created Admin group')
        else:
            self.stdout.write(f'Admin group already exists')

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
                    self.stdout.write(f'Added {action} permission for {model._meta.model_name} to Admin group')
                except Permission.DoesNotExist:
                    self.stdout.write(f'Permission {action}_{model._meta.model_name} does not exist')

        # EDITOR GROUP - Full permissions on LossOfProduction, view only on others
        editor_group, created = Group.objects.get_or_create(name="Editor")
        if created:
            self.stdout.write(f'Created Editor group')
        else:
            self.stdout.write(f'Editor group already exists')

        # Full permissions on LossOfProduction
        ct = ContentType.objects.get_for_model(LossOfProduction)
        for action in ["add", "change", "delete", "view"]:
            try:
                perm = Permission.objects.get(
                    content_type=ct,
                    codename=f"{action}_lossofproduction"
                )
                editor_group.permissions.add(perm)
                self.stdout.write(f'Added {action} permission for lossofproduction to Editor group')
            except Permission.DoesNotExist:
                self.stdout.write(f'Permission {action}_lossofproduction does not exist')

        # View only permissions on lookup models
        for model in lookup_models:
            ct = ContentType.objects.get_for_model(model)
            try:
                perm = Permission.objects.get(
                    content_type=ct,
                    codename=f"view_{model._meta.model_name}"
                )
                editor_group.permissions.add(perm)
                self.stdout.write(f'Added view permission for {model._meta.model_name} to Editor group')
            except Permission.DoesNotExist:
                self.stdout.write(f'Permission view_{model._meta.model_name} does not exist')

        # READER GROUP - View only permissions on all models
        reader_group, created = Group.objects.get_or_create(name="Reader")
        if created:
            self.stdout.write(f'Created Reader group')
        else:
            self.stdout.write(f'Reader group already exists')

        for model in all_models:
            ct = ContentType.objects.get_for_model(model)
            try:
                perm = Permission.objects.get(
                    content_type=ct,
                    codename=f"view_{model._meta.model_name}"
                )
                reader_group.permissions.add(perm)
                self.stdout.write(f'Added view permission for {model._meta.model_name} to Reader group')
            except Permission.DoesNotExist:
                self.stdout.write(f'Permission view_{model._meta.model_name} does not exist')

        self.stdout.write(
            self.style.SUCCESS('Successfully created permission groups!')
        )

        # Display summary
        self.stdout.write('\n--- Permission Summary ---')
        for group in [admin_group, editor_group, reader_group]:
            self.stdout.write(f'\n{group.name} Group:')
            for perm in group.permissions.all().order_by('content_type__model', 'codename'):
                self.stdout.write(f'  - {perm.content_type.model}: {perm.codename}')

# You'll also need to create the directories if they don't exist:
# mkdir -p lossofproduction/management/commands
# touch lossofproduction/management/__init__.py
# touch lossofproduction/management/commands/__init__.py