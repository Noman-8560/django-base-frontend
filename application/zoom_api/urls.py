from django.urls import path
from .views import *

app_name = 'zoom_api'
urlpatterns = [
    path('', zoom, name='zoom'),
    path('run/', run, name='run'),
    path('meeting/', meeting, name='meeting')
]
