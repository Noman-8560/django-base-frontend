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
    path('a/', include('src.portals.admins.urls', namespace='admin-portal')),
    path('s/', include('src.portals.student.urls', namespace='student-portal')),
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
