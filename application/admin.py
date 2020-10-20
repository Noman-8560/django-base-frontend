from django.contrib import admin
from application.models import *

admin.site.site_header = 'CoCognito | Admin'
admin.site.site_title = 'CoCognito | Admin'

admin.site.index_title = 'CoCognito | Tables'


class OptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'id']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']


class GuardianAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['statement', 'id', 'subject']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


class AttemptAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'successful', 'start_time', 'end_time', 'id']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz']


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Quiz, QuizAdmin)
