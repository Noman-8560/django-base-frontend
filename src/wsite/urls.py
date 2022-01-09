from django.urls import path
from .views import (
    HomeView, Error404View, LearningListView, QuizListView
)

app_name = "wsite"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quizzes/', QuizListView.as_view(), name='quizzes'),
    path('learning-resources/', LearningListView.as_view(), name='learning-resources'),
    path('404/', Error404View.as_view(), name='404'),
]