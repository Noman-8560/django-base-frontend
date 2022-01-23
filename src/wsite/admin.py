from django.contrib import admin
from .models import (
    Team, Content, Partner, Testimonial
)


admin.site.register(Team)
admin.site.register(Content)
admin.site.register(Partner)
admin.site.register(Testimonial)
