from django.urls import path, include

from src.portals.admins.views import (
    DashboardView,
    ArticleListView, ArticleDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDetailView,
    SubjectListView, SubjectDetailView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView,
    QuizListView, QuizCreateView, QuizUpdateView, QuizDeleteView, QuizDetailView,
    QuestionListView, QuestionCreateView, QuestionDeleteView, QuestionUpdateView,
    RelationListView, RelationCreateView, RelationUpdateView, RelationDeleteView,
    TopicListView, TopicCreateView, TopicUpdateView, TopicDeleteView,

    QuestionChoiceAddJSON, QuestionChoiceDeleteJSON, QuestionStatementAddJSON, QuestionStatementDeleteJSON,
    QuestionImageCreateView, QuestionImageDeleteView, QuestionAudioCreateView, QuestionAudioDeleteView,

    QuestionStatementStatusUpdateJSON, QuestionChoiceStatusUpdateJSON, QuestionImageStatusUpdateJSON,
    QuestionAudioStatusUpdateJSON, QuestionSubmitStatusUpdateJSON, QuizQuestionAddJSON, QuizQuestionDeleteJSON
)

app_name = "admin-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('article/', ArticleListView.as_view(), name='article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add/article/', ArticleCreateView.as_view(), name='article-create'),
    path('update/article/<int:pk>/', ArticleUpdateView.as_view(), name='article-update'),
    path('delete/article/<int:pk>/', ArticleDeleteView.as_view(), name='article-delete'),

    path('relation/', RelationListView.as_view(), name='relation'),
    path('add/relation/', RelationCreateView.as_view(), name='relation-create'),
    path('update/relation/<int:pk>/', RelationUpdateView.as_view(), name='relation-update'),
    path('delete/relation/<int:pk>/', RelationDeleteView.as_view(), name='relation-delete'),

    path('subject/', SubjectListView.as_view(), name='subject'),
    path('subject/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('add/subject/', SubjectCreateView.as_view(), name='subject-create'),
    path('update/subject/<int:pk>/', SubjectUpdateView.as_view(), name='subject-update'),
    path('delete/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),

    path('topic/', TopicListView.as_view(), name='topic'),
    path('add/topic/', TopicCreateView.as_view(), name='topic-create'),
    path('update/topic/<int:pk>/', TopicUpdateView.as_view(), name='topic-update'),
    path('delete/topic/<int:pk>/', TopicDeleteView.as_view(), name='topic-delete'),

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
