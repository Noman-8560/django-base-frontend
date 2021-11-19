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

    # -------------------------------------------------------------------------------------------------- JSON RESPONSES
    path('json/question_statement/add/', QuestionStatementAddJSON.as_view(), name='question-statement-add-json'),
    path('json/question_choice/add/', QuestionChoiceAddJSON.as_view(), name='question-choice-add-json'),
    path('json/question_statement/<int:pk>/delete/', QuestionStatementDeleteJSON.as_view(),
         name='question-statement-delete-json'),
    path('json/question_choice/<int:pk>/delete/', QuestionChoiceDeleteJSON.as_view(),
         name='question-choice-delete-json'),
    path('json/question_image/<int:question_id>/image/add/', QuestionImageCreateView.as_view(),
         name='question-image-create-json'),
    path('json/question_image/image/<int:pk>/delete/', QuestionImageDeleteView.as_view(),
         name='question-image-delete-json'),
    path('json/question_audio/<int:question_id>/audio/add/', QuestionAudioCreateView.as_view(),
         name='question-audio-create-json'),
    path('json/question_audio/<int:pk>/delete/', QuestionAudioDeleteView.as_view(), name='question-audio-delete-json'),

    path('json/quiz/question/statement/status/<int:pk>/change/', QuestionStatementStatusUpdateJSON.as_view(),
         name='question-statement-status-change-json'),
    path('json/quiz/question/choice/status/<int:pk>/change/', QuestionChoiceStatusUpdateJSON.as_view(),
         name='question-choice-status-change-json'),
    path('json/quiz/question/image/status/<int:pk>/change/', QuestionImageStatusUpdateJSON.as_view(),
         name='question-image-status-change-json'),
    path('json/quiz/question/audio/status/<int:pk>/change/', QuestionAudioStatusUpdateJSON.as_view(),
         name='question-audio-status-change-json'),
    path('json/quiz/question/submission/status/<int:pk>/change/', QuestionSubmitStatusUpdateJSON.as_view(),
         name='question-submission-status-change-json'),
    path('json/quiz/<int:quiz_id>/question/<int:question_id>/add/', QuizQuestionAddJSON.as_view(),
         name='quiz-question-add-json'),
    path('json/quiz/<int:quiz_id>/question/<int:question_id>/delete/', QuizQuestionDeleteJSON.as_view(),
         name='quiz-question-delete-json'),

]
