from django.contrib import admin
from django.apps import apps
from application.models import *

admin.site.site_header = 'CoCognito | Admin'
admin.site.site_title = 'CoCognito | Admin'

admin.site.index_title = 'CoCognito | Tables'

models = ['Choice', 'Subject', 'Attempt', 'Team', 'Quiz']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'statement']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

for model in models:
    admin.site.register(apps.get_model('application.' + model))
