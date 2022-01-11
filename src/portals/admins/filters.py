import django_filters
from django.forms import TextInput

from src.accounts.models import User
from src.application.models import Quiz, StudentGrade


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
    age_limit = django_filters.NumberFilter(widget=TextInput(attrs={'placeholder': 'Maximum Age'}), lookup_expr='lte')
    start_time = django_filters.DateTimeFilter(widget=TextInput(attrs={'placeholder': 'Start Time'}), lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(widget=TextInput(attrs={'placeholder': 'End Time'}), lookup_expr='lte')
    grade = django_filters.ModelChoiceFilter(queryset=StudentGrade.objects.all())

    class Meta:
        model = Quiz
        fields = {}
