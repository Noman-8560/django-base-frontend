import notifications.urls
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [

    # BASE URLS -------------------------------------------------------- #

    # REQUIRED --------------------------------------------------------- #
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('a/', include('src.portals.admins.urls', namespace='admin-portal')),
    path('s/', include('src.portals.student.urls', namespace='student-portal')),
    path('m/', include('src.portals.moderator.urls', namespace='moderator-portal')),
    path('p/', include('src.portals.parent.urls', namespace='parent-portal')),

    # DEPRECATED ------------------------------------------------------- #
    path('', include('src.application.urls', namespace='application')),
    path('zoom/', include('src.zoom_api.urls', namespace='zoom_api')),

    # NOTIFICATION SERVER ---------------------------------------------- #
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
