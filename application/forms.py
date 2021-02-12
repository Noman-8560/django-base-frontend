from django.contrib.admin.widgets import AdminSplitDateTime, AdminTimeWidget
from django.forms import *
from django import forms
from .models import *
from django.contrib.admin import widgets


class CSDateTimeInput(forms.DateTimeInput):
    input_type = 'da'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['id', 'subject', 'question_type', 'age_limit']


class QuestionStatementForm(ModelForm):
    class Meta:
        model = QuestionStatement
        fields = ['statement', 'screen']


class QuestionImageForm(ModelForm):
    class Meta:
        model = QuestionImage
        fields = ['url', 'image', 'screen']


class QuestionAudioForm(ModelForm):
    class Meta:
        model = QuestionAudio
        fields = ['url', 'audio', 'screen']


class QuestionChoiceForm(ModelForm):
    class Meta:
        model = QuestionChoice
        fields = ['text', 'is_correct']


''' QUIZ BUILDER VIEWS _______________________________________________________________'''


class QuizForm(ModelForm):
    start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = Quiz
        fields = ['learning_purpose', 'title', 'age_limit', 'players', 'submission_control', 'subjects', 'start_time', 'end_time']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['topic', 'event', 'content', 'content', 'active']


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'participants', 'is_active']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class ProfileImageForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile']


class ProfileBasicForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileZoomForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['zoom_account']


class ProfileOtherForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['gender', 'phone', 'date_of_birth', 'about', 'address']


class ProfileSchoolForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['school_name', 'class_name', 'class_section', 'school_email', 'school_address']


class ProfileParentForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['guardian_first_name', 'guardian_last_name', 'guardian_email']
