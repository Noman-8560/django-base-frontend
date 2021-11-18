from django.urls import path
from .views import CrossAuthView, IdentificationCheckView, ProfileUpdateView, ProfileImageUpdateView

app_name = "accounts"
urlpatterns = [
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth-view'),
    path('identification-check/', IdentificationCheckView.as_view(), name='identification-check'),
    path('profile/change/', ProfileUpdateView.as_view(), name='profile-change'),
    path('profile/image/change/', ProfileImageUpdateView.as_view(), name='profile-image-change'),
]
