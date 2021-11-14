from django.urls import path
from .views import event, article, articles, site_builder, home, page_404, page_500, coming_soon

app_name = 'wsite'
urlpatterns = [
    path('event/<slug:slug>/', event, name='event'),
    path('article/<slug:slug>/', article, name='article'),
    path('articles/', articles, name='articles'),
    path('builder/', site_builder, name='site_builder'),
    path('coming_soon/', coming_soon, name='coming_soon'),
    path('404/', page_404, name='404'),
    path('500/', page_500, name='500'),
]
