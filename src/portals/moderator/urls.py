from django.urls import path
from .views import (
    QuizListView, QuizCreateView, QuizDeleteView, QuizUpdateView, QuizDetailView,
    QuestionListView, QuestionCreateView, QuestionDeleteView, QuestionUpdateView
)

app_name = "moderator-portal"
urlpatterns = [

    path('quiz/', QuizListView.as_view(), name='quiz'),

    path('add/quiz/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('update/quiz/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'),
    path('delete/quiz/<int:pk>/', QuizDeleteView.as_view(), name='quiz-delete'),

    path('question/', QuestionListView.as_view(), name='question'),
    path('question/add/', QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/change/', QuestionUpdateView.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),

]
