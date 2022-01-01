from django.contrib.auth.models import User
from django.forms import *
from django import forms
from src.application.models import (
    Question, QuestionStatement, QuestionImage, QuestionAudio, QuestionChoice, Quiz, QuizQuestion, Article, Team,
    Subject
)


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
        fields = ['url', 'image']


class QuestionAudioForm(ModelForm):
    class Meta:
        model = QuestionAudio
        fields = ['url', 'audio']


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
        fields = ['learning_purpose', 'title', 'age_limit', 'players', 'subjects', 'start_time', 'end_time']


class QuizQuestionForm(ModelForm):

    class Meta:
        model = QuizQuestion
        fields = ['submission_control']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['topic', 'event', 'content', 'content', 'active']


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


