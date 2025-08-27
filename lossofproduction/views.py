from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
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
from .permissions import LookupModelPermissions, LossOfProductionPermissions


class BaseCRViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Base viewset that allows Create and Read operations"""
    pass


class LookupCRUDViewSet(viewsets.ModelViewSet):
    """Full CRUD viewset for lookup models with permission control"""
    permission_classes = [IsAuthenticated, LookupModelPermissions]


class DepartmentViewSet(LookupCRUDViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class AffectedAreaViewSet(LookupCRUDViewSet):
    queryset = AffectedArea.objects.all()
    serializer_class = AffectedAreaSerializer


class CauseViewSet(LookupCRUDViewSet):
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer


class ReportingLimitAreaViewSet(LookupCRUDViewSet):
    queryset = ReportingLimitArea.objects.select_related("department").all()
    serializer_class = ReportingLimitAreaSerializer


class LossOfProductionViewSet(viewsets.ModelViewSet):
    """Full CRUD viewset for LossOfProduction with permission control"""
    permission_classes = [IsAuthenticated, LossOfProductionPermissions]
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