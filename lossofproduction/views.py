from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import (
    Department,
    AffectedArea,
    Cause,
    ReportingLimitArea,
    LossOfProduction,
)
from .serializers import (
    DepartmentSerializer,
    AffectedAreaSerializer,
    CauseSerializer,
    ReportingLimitAreaSerializer,
    LossOfProductionSerializer,
)


class BaseCRViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class DepartmentViewSet(BaseCRViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class AffectedAreaViewSet(BaseCRViewSet):
    queryset = AffectedArea.objects.all()
    serializer_class = AffectedAreaSerializer

class CauseViewSet(BaseCRViewSet):
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer

class ReportingLimitAreaViewSet(BaseCRViewSet):
    queryset = ReportingLimitArea.objects.select_related("department").all()
    serializer_class = ReportingLimitAreaSerializer

class LossOfProductionViewSet(BaseCRViewSet):
    queryset = (
        LossOfProduction.objects
        .select_related("department", "affected_area", "cause", "reporting_limit_area__department")
        .order_by("-issue_date", "-id")
    )
    serializer_class = LossOfProductionSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response(
        {
            "username": user.username,
            "groups": list(user.groups.values_list("name", flat=True)),
            "permissions": list(user.get_all_permissions()),
        }
    )
