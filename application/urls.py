
from django.urls import path
from .views import (
    home, signup, login, parent_login,
    profile_update, quiz_user_1, quiz_user_2, quiz_user_3,
    help_view, quiz_builder, question_builder
)

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
    path('question/builder/', question_builder, name='question_builder'),

]