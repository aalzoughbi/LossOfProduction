from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lossofproduction.views import (
    DepartmentViewSet,
    AffectedAreaViewSet,
    CauseViewSet,
    ReportingLimitAreaViewSet,
    LossOfProductionViewSet,
    current_user,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"affected-areas", AffectedAreaViewSet, basename="affectedarea")
router.register(r"causes", CauseViewSet, basename="cause")
router.register(r"reporting-limit-areas", ReportingLimitAreaViewSet, basename="rla")
router.register(r"lossofproduction", LossOfProductionViewSet, basename="lop")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/me/", current_user, name="current_user"),
    # JWT auth endpoints
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
