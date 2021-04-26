from django.urls import path
from .views import event, article, articles, site_builder, home

app_name = 'wsite'
urlpatterns = [
    path('event/<slug:slug>/', event, name='event'),
    path('article/<slug:slug>/', article, name='article'),
    path('articles/', articles, name='articles'),
    path('builder/', site_builder, name='site_builder'),
]
