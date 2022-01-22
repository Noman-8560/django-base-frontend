from django.contrib import admin
from src.application.models import *
from allauth.account.models import EmailConfirmation
from django.contrib.sessions.models import Session

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
    fieldsets = (
        (None, {'fields': ('age_limit', 'grade', 'level', 'subject', 'topics', 'question_type')}),
        ('Quiz Statistics', {'fields': (
            'total_times_used_in_quizzes', 'total_times_attempted_in_quizzes', 'total_times_correct_in_quizzes'
        )}),
        ('Learning Statistics', {'fields': (
            'total_times_used_in_learning', 'total_times_attempted_in_learning', 'total_times_correct_in_learning'
        )}),
        ('Creation', {'fields': ('created_by',)}),
        ('Misc', {'fields': ('submission_control', 'choices_control')}),
    )
    list_display = ['id', 'age_limit', 'grade']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']


class AttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'question', 'user', 'quiz', 'team', 'successful', 'start_time', 'end_time']
    list_filter = ('quiz', 'question', 'team', 'successful', 'user')


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz']


class QuizAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'description', 'thumbnail', 'age_limit')}),
        ('Linked', {'fields': (
            'subjects', 'grade', 'players', 'topics'
        )}),
        ('Quiz Statistics', {'fields': (
            'total_enrolled_teams', 'total_enrolled_students', 'total_attempted_students', 'total_passed_student'
        )}),
        ('Author and Dates', {'fields': (
            'created_by', 'start_time', 'end_time'
        )}),
        ('Misc', {'fields': ('submission_control',)}),
    )
    list_display = ['title', 'start_time', 'end_time']


class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'question']


class QuestionStatementAdmin(admin.ModelAdmin):
    list_display = ['question', 'statement', 'screen']


class ScreenAdmin(admin.ModelAdmin):
    list_display = ['pk', 'no', 'name']


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'no_of_players', 'name']


class QuestionAudioAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'audio', 'question']


class QuestionImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'image', 'question']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'topic', 'event', 'active']


class AppUpdateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'url', 'status', 'active']


class QuizCompletedAdmin(admin.ModelAdmin):
    list_display = ['pk', 'quiz', 'user', 'total', 'passed', 'skipped', 'obtained', 'remains', 'created']


class LearningResourceResultAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'attempts', 'total', 'obtained', 'created']


class LearningResourceAttemptsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'question', 'successful', 'start_time', 'end_time']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'is_guardian', 'gender', 'phone']


class ChoiceVisibilityAdmin(admin.ModelAdmin):
    list_display = ['pk', 'quiz_question', 'choice', 'screen_1', 'screen_2', 'screen_3']


class StatementVisibilityAdmin(admin.ModelAdmin):
    list_display = ['pk', 'quiz_question', 'statement', 'screen_1', 'screen_2', 'screen_3']


admin.site.register(StatementVisibility, StatementVisibilityAdmin)
admin.site.register(ChoiceVisibility, ChoiceVisibilityAdmin)
admin.site.register(QuestionAudio, QuestionAudioAdmin)
admin.site.register(QuestionImage, QuestionImageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(QuestionStatement, QuestionStatementAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Quiz, QuizAdmin)

admin.site.register(AppUpdate, AppUpdateAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(QuizCompleted, QuizCompletedAdmin)
admin.site.register(LearningResourceAttempts, LearningResourceAttemptsAdmin)
admin.site.register(LearningResourceResult, LearningResourceResultAdmin)

admin.site.register(EmailConfirmation)
admin.site.register(Session)
admin.site.register(QuizQuestion)
admin.site.register(QuizMisc)
admin.site.register(RelationType)
admin.site.register(Relation)
