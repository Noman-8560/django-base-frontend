from django.urls import path, include

from src.portals.admins.views import (
    DashboardView,
)

app_name = "admin-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]
