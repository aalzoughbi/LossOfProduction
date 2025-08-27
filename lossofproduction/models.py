from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class AffectedArea(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cause(models.Model):
    name = models.CharField(max_length=160, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ReportingLimitArea(models.Model):
    name = models.CharField(max_length=160, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='reporting_limit_areas')

    class Meta:
        unique_together = ('name', 'department')
        ordering = ['department__name', 'name']

    def __str__(self):
        return f'{self.name} ({self.department})'


class LossOfProduction(models.Model):
    class EventType(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        UNPLANNED = 'UNPLANNED', 'Unplanned'

    class Status(models.TextChoices):
        FINISHED = 'FINISHED', 'Finished'
        ONGOING = 'ONGOING', 'Ongoing'
        NO_SELECTION = 'NO_SELECTION', 'No-Selection'

    id = models.AutoField(primary_key=True)
    issue_date = models.DateField(default=timezone.localdate)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='loss_events')
    affected_area = models.ForeignKey(AffectedArea, on_delete=models.PROTECT, related_name='loss_events')
    equipment_or_process_step = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cause = models.ForeignKey(Cause, on_delete=models.PROTECT, related_name='loss_events')
    event_type = models.CharField(max_length=10, choices=EventType.choices)
    status = models.CharField(max_length=12, choices=Status.choices)
    date_solved = models.DateField(blank=True, null=True)
    reporting_limit_area = models.ForeignKey(ReportingLimitArea, on_delete=models.PROTECT, related_name='loss_events')
    reporting_limit = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-issue_date', '-id']
        verbose_name = 'Loss of Production'
        verbose_name_plural = 'Loss of Production'

    def __str__(self):
        return f'Loss #{self.id} - {self.issue_date} - {self.department}'

    def clean(self):
        """
        Enforce that the selected reporting_limit_area belongs to the selected department.
        """
        super().clean()
        if(
            self.reporting_limit_area
            and self.department
            and self.reporting_limit_area.department_id != self.department_id
        ):
            from django.core.exceptions import ValidationError
            raise ValidationError(
                {'reporting_limit_area': f'The selected reporting_limit_area ({self.reporting_limit_area}) does not belong to the selected department ({self.department}).'}
            )