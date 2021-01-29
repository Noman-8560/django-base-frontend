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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

import notifications.urls

from . import settings
from django.urls import path, include
from django.views.generic import TemplateView
from application.wsite.views import home

from agora.views import Agora

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('login/', TemplateView.as_view(template_name="account/login.html")),

    path('', home, name='home'),
    path('', include('application.urls', namespace='application')),
    path('site/', include('application.wsite.urls', namespace='wsite')),
    path('zoom/', include('application.zoom_api.urls', namespace='zoom_api')),

    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('agora/', Agora.as_view(
        app_id='3a0052057f624f22ab2fb903f1b02d2d',
        channel='marks_man'
    )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
