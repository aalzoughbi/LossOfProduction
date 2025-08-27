from django.contrib import admin
from .models import *


@admin.register(Department, AffectedArea, Cause, ReportingLimitArea)
class SimpleLookupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(LossOfProduction)
class LossOfProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_date', 'department', 'affected_area', 'event_type', 'status', 'date_solved',)
    list_filter = ('department', 'affected_area', 'event_type', 'status', 'cause',)
    search_fields = ('id', 'equipment_or_process_step', 'description', 'reporting_limit',)
    autocomplete_fields = ('department', 'affected_area', 'cause', 'reporting_limit_area',)