from rest_framework import serializers
from .models import (
    Department,
    AffectedArea,
    Cause,
    ReportingLimitArea,
    LossOfProduction,
)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]

class AffectedAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectedArea
        fields = ["id", "name"]

class CauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cause
        fields = ["id", "name"]

class ReportingLimitAreaSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )

    class Meta:
        model = ReportingLimitArea
        fields = ["id", "name", "department"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["department"] = instance.department.name
        return data

class LossOfProductionSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )
    affected_area = serializers.PrimaryKeyRelatedField(
        queryset=AffectedArea.objects.all()
    )
    cause = serializers.PrimaryKeyRelatedField(queryset=Cause.objects.all())
    reporting_limit_area = serializers.PrimaryKeyRelatedField(
        queryset=ReportingLimitArea.objects.all()
    )

    class Meta:
        model = LossOfProduction
        fields = [
            "id",
            "issue_date",
            "department",
            "affected_area",
            "equipment_or_process_step",
            "description",
            "cause",
            "event_type",
            "status",
            "date_solved",
            "reporting_limit_area",
            "reporting_limit",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {
                "department": instance.department.name,
                "affected_area": instance.affected_area.name,
                "cause": instance.cause.name,
                "reporting_limit_area": f"{instance.reporting_limit_area.name} ({instance.reporting_limit_area.department.name})",
                "event_type": instance.get_event_type_display(),
                "status": instance.get_status_display(),
            }
        )
        return data
