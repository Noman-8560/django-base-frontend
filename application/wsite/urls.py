from django.urls import path
from .views import event, article, articles

app_name = 'wsite'
urlpatterns = [
    path('event/<slug:slug>/', event, name='event'),
    path('article/<slug:slug>/', article, name='article'),
    path('articles/', articles, name='articles'),
]
