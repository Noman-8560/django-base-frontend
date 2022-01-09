from django.urls import path
from .views import (
    HomeView, Error404View, LearningListView, QuizListView, PrivacyPolicyView, TermsAndConditionsView
)

app_name = "wsite"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quizzes/', QuizListView.as_view(), name='quizzes'),
    path('learning-resources/', LearningListView.as_view(), name='learning-resources'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('404/', Error404View.as_view(), name='404'),
]