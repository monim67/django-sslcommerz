from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from .views import (
    SessionDetailView,
    IpnView,
    SuccessView,
    FailView,
    CancelView,
)


app_name = "django_sslcommerz"

urlpatterns = [
    path("session", SessionDetailView.as_view(), name="session.detail"),
    path("ipn", csrf_exempt(IpnView.as_view()), name="ipn"),
    path("success", csrf_exempt(SuccessView.as_view()), name="success"),
    path("fail", csrf_exempt(FailView.as_view()), name="fail"),
    path("cancel", csrf_exempt(CancelView.as_view()), name="cancel"),
]
