from django.urls import path
from .views import (
    DashboardView,
    ChildListView, ChildDetailView, ChildCreateView, ChildUpdateView, ChildDeleteView
)

app_name = "parent-portal"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('child/', ChildListView.as_view(), name='child'),
    path('child/add/', ChildCreateView.as_view(), name='child-create'),
    path('child/<int:pk>/', ChildDetailView.as_view(), name='child-detail'),
    path('child/<int:pk>/update/', ChildUpdateView.as_view(), name='child-update'),
    path('child/<int:pk>/delete/', ChildDeleteView.as_view(), name='child-delete'),

]
