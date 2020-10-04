
from django.urls import path
from .views import home

app_name = 'application'
urlpatterns = [
    path('', home, name='home'),
]