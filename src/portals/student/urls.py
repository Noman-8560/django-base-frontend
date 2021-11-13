from django.urls import path
from .views import (
    DashboardView, QuizListView, TeamListView, LearningResourceListView
)


app_name = "student-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('quiz/', QuizListView.as_view(), name='quiz'),
    path('team/', TeamListView.as_view(), name='team'),
    path('learning-resource/', LearningResourceListView.as_view(), name='learning-resource'),

    # -------------------------------------------------------------------------------------------------- JSON RESPONSES
]
