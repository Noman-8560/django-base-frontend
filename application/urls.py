from django.urls import path
from .views import *

app_name = 'application'
urlpatterns = [
    path('', help_view, name='help'),

    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('parent/login/', parent_login, name='parent_login'),
    path('profile/update/', profile_update, name='profile_update'),
    path('quiz/user/1/', quiz_user_1, name='quiz_user_1'),
    path('quiz/user/2/', quiz_user_2, name='quiz_user_2'),
    path('quiz/user/3/', quiz_user_3, name='quiz_user_3'),
    path('quiz/builder/', quiz_builder, name='quiz_builder'),
    path('learning_resource/', learning_resource, name='learning_resource'),
    path('learning_resource_quiz/', learning_resource_quiz, name='learning_resource_quiz'),

    path('question/builder/', question_builder, name='question_builder'),
    path('question/<int:pk>/', question_builder_update, name='question_builder_update'),

    path('add/statement/for/question/<int:question>/', question_statement_add, name='question_statement_add'),
    path('delete/statement/<int:pk>/', question_statement_delete, name='question_statement_delete'),

    path('add/choice/for/question/<int:question>/', question_choices_add, name='question_choice_add'),
    path('delete/choice/<int:pk>/', question_choice_delete, name='question_choice_delete'),

    path('add/image/for/question/<int:question>/', question_image_add, name='question_image_add'),
    path('delete/image/<int:pk>/', question_image_delete, name='question_image_delete'),

    path('add/audio/for/question/<int:question>/', question_audio_add, name='question_audio_add'),
    path('delete/audio/<int:pk>/', question_audio_delete, name='question_audio_delete'),
]