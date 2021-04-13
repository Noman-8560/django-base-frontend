from django.urls import path, include
from .views import *

app_name = 'application'
urlpatterns = [
    #  --- HELP_PAGE

    path('help/', help_view, name='help'),
    path('dashboard/', dashboard, name='dashboard'),

    path('articles/', articles, name='articles'),
    path('add/article/', add_article, name='add_article'),
    path('update/article/<int:pk>/', add_article, name='update_article'),
    path('delete/article/<int:pk>/', delete_article, name='delete_article'),

    path('profile/', profile_update, name='profile_update'),
    path('zoom/profile/', zoom_profile, name='zoom_profile'),

    path('subjects/', subjects, name='subjects'),
    path('add/subject/', add_subject, name='add_subject'),
    path('update/subject/<int:pk>/', update_subject, name='update_subject'),
    path('delete/subject/<int:pk>/', delete_subject, name='delete_subject'),

    # --- QUIZ SETUP
    path('quizzes/', quizzes, name='quizzes'),
    path('quiz/builder/', quiz_builder, name='quiz_builder'),
    path('update/quiz/<int:pk>/', update_quiz, name='update_quiz'),
    path('delete/quiz/<int:pk>/', delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz>/start/', quiz_start, name='quiz_start'),
    path('quiz/<int:pk>/', quiz_builder_update, name='quiz_builder_update'),

    path('learn/quiz/<int:quiz>/', learning_resources_start, name='learning_resource_start'),
    path('learning_resources/', learning_resources, name='learning_resources'),
    path('learning_resource/result/quiz/<int:quiz>/', learning_resources_result, name='learning_resource_result'),

    path('quizes/', quizes, name='quizes'),
    path('teams/', teams, name='teams'),
    path('admin/teams/', admin_teams, name='admin_teams'),
    path('admin/delete/team/<int:pk>/', admin_team_delete, name='admin_team_delete'),
    path('team/<int:pk>/', team, name='team'),
    path('enroll/quiz/<int:pk>/', enroll, name='enroll_quiz'),

    path('delete/team/<int:pk>/', delete_team, name='delete_team'),

    # --- QUESTION BUILDER
    path('questions/', questions, name='questions'),
    path('question/builder/', question_builder, name='question_builder'),
    path('update/question/<int:pk>/', update_question, name='update_question'),
    path('delete/question/<int:pk>/', delete_question, name='delete_question'),
    path('question/<int:pk>/', question_builder_update, name='question_builder_update'),

    path(
        'update/screen/option/<int:option>/question/<int:question>/',
        quiz_builder_question_submission_control,
        name='quiz_builder_question_submission_control'
    ),
    path('search/questions/for/quiz/<int:quiz_pk>/', search_question, name='search_question'),
    path('add/statement/for/question/<int:question>/', question_statement_add, name='question_statement_add'),
    path('add/question_statement/', add_question_statement, name='add_question_statement'),
    path('add/question_choice/', add_question_choice, name='add_question_choice'),
    path('delete/question_statement/<int:pk>/', delete_question_statement, name='delete_question_statement'),
    path('delete/question_choice/<int:pk>/', delete_question_choice, name='delete_question_choice'),
    path('delete/statement/<int:pk>/', question_statement_delete, name='question_statement_delete'),
    path('add/choice/for/question/<int:question>/', question_choices_add, name='question_choice_add'),
    path('delete/choice/<int:pk>/', question_choice_delete, name='question_choice_delete'),
    path('add/image/for/question/<int:question>/', question_image_add, name='question_image_add'),
    path('delete/image/<int:pk>/', question_image_delete, name='question_image_delete'),
    path('add/audio/for/question/<int:question>/', question_audio_add, name='question_audio_add'),
    path('delete/audio/<int:pk>/', question_audio_delete, name='question_audio_delete'),

    path('add/quiz/<int:quiz>/question/<int:question>/', quiz_question_add, name='quiz_question_add'),
    path('delete/quiz/<int:quiz>/question/<int:question>/', quiz_question_delete, name='quiz_question_delete'),

    path('coming_soon/', coming_soon, name='coming_soon'),
    path('404/', page_404, name='404'),
    path('500/', page_500, name='500'),
    path('results/', results, name='results'),

    # --- C-API
    path('c/api/user/<str:username>/exists/', user_exists_json, name='capi_user_exists'),
    path('c/api/submit/question/', question_submission_json, name='capi_question_submission'),
    path('c/api/next/question/', next_question_json, name='capi_next_question'),
    path('c/api/quiz/<int:quiz_id>/question/<int:question_id>/num/<int:user_id>/skip/<int:skip>/',
         quiz_access_question_json,
         name='capi_quiz_question_access'),

    path('c/api/learn/<int:quiz_id>/question/<int:question_id>/', learn_access_question_json,
         name='capi_learn_question_access'),
    path('c/api/learn/submit/question/', learn_question_submission_json, name='capi_learn_question_submission'),
]
