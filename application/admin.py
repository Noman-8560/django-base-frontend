from django.contrib import admin
from application.models import *

admin.site.site_header = 'CoCognito | Admin'
admin.site.site_title = 'CoCognito | Admin'

admin.site.index_title = 'CoCognito | Tables'


class OptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'id', 'created_on']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created_on']


class GuardianAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'created_on']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['statement', 'id', 'subject', 'created_on']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'created_on']


class AttemptAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'successful', 'start_time', 'end_time', 'created_on', 'id']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz', 'created_on']


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'created_on']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Quiz, QuizAdmin)
