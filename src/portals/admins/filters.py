import django_filters
from django.forms import TextInput

from src.accounts.models import User
from src.application.models import Quiz


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}), lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {
            'is_active': ['exact']
        }


class QuizFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Quiz Title'}), lookup_expr='icontains')
    age_limit = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Age Limit'}), lookup_expr='icontains')

    class Meta:
        model = Quiz
        fields = {
            'grade': ['exact'],
        }