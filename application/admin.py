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
    list_display = ['id', 'subject', 'submission_control', 'choices_control']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


class AttemptAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'successful', 'start_time', 'end_time', 'id']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz']


class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time']


class QuestionOptionsAdmin(admin.ModelAdmin):
    list_display = ['question', 'option', 'is_correct']


class QuestionStatementAdmin(admin.ModelAdmin):
    list_display = ['question', 'statement', 'screen']


class ScreenAdmin(admin.ModelAdmin):
    list_display = ['pk', 'no', 'name']


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'no_of_players', 'name']


class QuestionAudioAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'audio', 'screen', 'question']


class QuestionImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'image', 'screen', 'question']


admin.site.register(QuestionAudio, QuestionAudioAdmin)
admin.site.register(QuestionImage, QuestionImageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(QuestionStatement, QuestionStatementAdmin)
admin.site.register(QuestionOption, QuestionOptionsAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Quiz, QuizAdmin)
