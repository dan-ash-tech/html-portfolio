from django.urls import path
from .views import dashboard, scan_network_view


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("scan/", scan_network_view, name="scan_network"),
]