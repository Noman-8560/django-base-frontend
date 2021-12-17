from django.urls import path
from .views import (
    DashboardView, ChildDetailView, ChildQuizDetailView, ChildLearningDetailView,
    RelationListView, RelationDetailView, RelationCreateView, RelationUpdateView, RelationDeleteView
)

app_name = "parent-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('relation/', RelationListView.as_view(), name='relation'),
    path('relation/add/', RelationCreateView.as_view(), name='relation-create'),
    path('relation/<int:pk>/', RelationDetailView.as_view(), name='relation-detail'),
    path('relation/<int:pk>/update/', RelationUpdateView.as_view(), name='relation-update'),
    path('relation/<int:pk>/delete/', RelationDeleteView.as_view(), name='relation-delete'),

    path('child/<int:pk>/', ChildDetailView.as_view(), name='child-detail'),
    path('child/<int:relation_id>/quiz/<int:pk>/', ChildQuizDetailView.as_view(), name='child-quiz-detail'),
    path('child/<int:relation_id>/learn/<int:pk>/', ChildLearningDetailView.as_view(), name='child-learn-detail'),

]
