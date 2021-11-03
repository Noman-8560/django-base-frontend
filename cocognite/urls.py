"""cocognite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from src.wsite.views import home
from . import settings

urlpatterns = [

    # REQUIRED --------------------------------------------------------- #
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('admins/', include('src.portals.admins.urls', namespace='admin-portal')),
    # path('s/', include('src.student.admins.urls', namespace='student-portal')),
    # path('m/', include('src.moderator.admins.urls', namespace='moderator-portal')),
    # path('p/', include('src.parent.admins.urls', namespace='parent-portal')),

    # DEPRECATED ------------------------------------------------------- #
    path('', include('src.application.urls', namespace='application')),
    path('site/', include('src.wsite.urls', namespace='wsite')),
    path('zoom/', include('src.zoom_api.urls', namespace='zoom_api')),

    # NOTIFICATION SERVER ---------------------------------------------- #
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
