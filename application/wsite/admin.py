from django.contrib import admin
from .models import WebsiteEvents, WebsiteModules, WebsiteTeam, Website

# Register your models here.

admin.site.register(WebsiteModules)
admin.site.register(WebsiteTeam)
admin.site.register(WebsiteEvents)
admin.site.register(Website)
