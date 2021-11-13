from django.urls import path
from .views import (
    DashboardView, QuizListView, TeamListView, ZoomMeetingView, QuizEnrollView, QuizLiveView,
    LearningResourceListView, LearningResourceLiveView, LearningResourceResultView,

    LearningResourceLiveQuestionAccessJSON, LearningResourceLiveQuestionSubmitJSON,
    QuizLiveQuestionNextJSON, QuizLiveQuestionAccessJSON, QuizLiveQuestionSubmitJSON, UserExistsJSON
)

app_name = "student-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('team/', TeamListView.as_view(), name='team'),

    path('quiz/', QuizListView.as_view(), name='quiz'),
    path('quiz/<int:pk>/live/', QuizLiveView.as_view(), name='quiz-live'),
    path('quiz/<int:pk>/enroll/', QuizEnrollView.as_view(), name='quiz-enroll'),

    path('learning-resource/', LearningResourceListView.as_view(), name='learning-resource'),
    path('learning-resource/<int:quiz_id>/live/', LearningResourceLiveView.as_view(), name='learning-resource-live'),
    path('learning-resource/<int:quiz_id>/result/', LearningResourceResultView.as_view(),
         name='learning-resource-result'),

    path('zoom/<int:quiz>/', ZoomMeetingView, name='zoom-meeting'),

    # -------------------------------------------------------------------------------------------------- JSON RESPONSES
    path('json/learning-resource/live/access/question/<int:question_id>/quiz/<int:quiz_id>/',
         LearningResourceLiveQuestionAccessJSON, name='learning-resource-live-access-question-json'),
    path('json/learning-resource/live/submit/question', LearningResourceLiveQuestionSubmitJSON,
         name='learning-resource-live-submit-question-json'),
    path('json/user/<str:username>/exists/', UserExistsJSON.as_view(), name='user-exists-json'),

    path('json/quiz/live/question/submit/', QuizLiveQuestionSubmitJSON.as_view(), name='capi_question_submission'),
    path('json/quiz/live/question/next/', QuizLiveQuestionNextJSON.as_view(), name='capi_next_question'),
    path('json/quiz/<int:quiz_id>/question/<int:question_id>/num/<int:user_id>/skip/<int:skip>/',
         QuizLiveQuestionSubmitJSON.as_view(), name='capi_quiz_question_access'
    ),
]
