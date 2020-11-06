from django.forms import ModelForm
from application.models import Question


class QuestionsForm(ModelForm):
    class Meta:
        model = Question
        fields = (
            'statement',
            'subject',
            'hint',
            'image_hint_url',
            'audio_hint_url',
            'image_hint_file',
            'audio_hint_file',
        )
