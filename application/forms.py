from django.forms import ModelForm, HiddenInput
from .models import *


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