from django.urls import path
from .views import (
    DashboardView, QuizListView, TeamListView,
    LearningResourceListView, LearningResourceLiveView, LearningResourceResultView,

    LearningResourceLiveQuestionAccessJSON, LearningResourceLiveQuestionSubmitJSON
)

app_name = "student-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('team/', TeamListView.as_view(), name='team'),

    path('quiz/', QuizListView.as_view(), name='quiz'),

    path('learning-resource/', LearningResourceListView.as_view(), name='learning-resource'),
    path('learning-resource/<int:quiz_id>/live/', LearningResourceLiveView.as_view(), name='learning-resource-live'),
    path('learning-resource/<int:quiz_id>/result/', LearningResourceResultView.as_view(),
         name='learning-resource-result'),

    # -------------------------------------------------------------------------------------------------- JSON RESPONSES
    path('json/learning-resource/live/access/question/<int:question_id>/quiz/<int:quiz_id>/',
         LearningResourceLiveQuestionAccessJSON, name='learning-resource-live-access-question-json'),
    path('json/learning-resource/live/submit/question', LearningResourceLiveQuestionSubmitJSON,
         name='learning-resource-live-submit-question-json'),
]
