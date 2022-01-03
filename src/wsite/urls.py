from django.urls import path
from .views import (
    HomeView, Error404View
)

app_name = "wsite"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('404/', Error404View.as_view(), name='home'),
]