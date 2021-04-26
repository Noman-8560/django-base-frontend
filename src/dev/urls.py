from django.urls import path
from .views import (
    home, add_discussion, update_discussion, satisfied_discussion, logout_view, login_view,
    discussions, delete_discussion, discussion, add_answer, update_answer, delete_answer
)

app_name = 'dev'
urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),

    path('discussions/', discussions, name='discussions'),
    path('discussion/<int:discussion_id>/', discussion, name='discussion'),

    path('add/discussion/', add_discussion, name='add_discussion'),
    path('update/discussion/<int:discussion_id>/', update_discussion, name='update_discussion'),
    path('delete/discussion/<int:discussion_id>/', delete_discussion, name='delete_discussion'),

    path('add/answer/to/discussion/<int:discussion_id>/', add_answer, name='add_answer_to_discussion'),
    path('update/answer/<int:answer_id>/of/discussion/<int:discussion_id>/', update_answer, name='update_answer_of_discussion'),
    path('delete/answer/<int:answer_id>/of/discussion/<int:discussion_id>/', delete_answer, name='delete_answer_of_discussion'),
    path('satisfied/discussion/<int:discussion_id>/', satisfied_discussion, name='satisfied_discussion'),
]
