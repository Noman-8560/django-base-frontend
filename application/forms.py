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
         fields = ['subject', 'submission_control', 'choices_control', 'age_limit']


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
        fields = ['title', 'age_limit', 'subjects', 'age_limit', 'start_time', 'end_time']


