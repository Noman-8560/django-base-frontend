from django.urls import path, include

from src.portals.admins.views import (
    DashboardView, ArticleListView, ArticleDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDetailView,
    SubjectListView, SubjectDetailView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView
)

app_name = "admin-portal"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('article/', ArticleListView.as_view(), name='article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add/article/', ArticleCreateView.as_view(), name='article-create'),
    path('update/article/<int:pk>/', ArticleUpdateView.as_view(), name='article-update'),
    path('delete/article/<int:pk>/', ArticleDeleteView.as_view(), name='article-delete'),

    path('subject/', SubjectListView.as_view(), name='subject'),
    path('subject/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('add/subject/', SubjectCreateView.as_view(), name='subject-create'),
    path('update/subject/<int:pk>/', SubjectUpdateView.as_view(), name='subject-update'),
    path('delete/subject/<int:pk>/', SubjectDeleteView.as_view(), name='subject-delete'),

]
