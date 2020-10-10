
from django.urls import path
from .views import (
    home, signup, login, parent_login, profile_update
)

app_name = 'application'
urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('parent/login/', parent_login, name='parent_login'),
    path('profile/update/', profile_update, name='profile_update'),
]