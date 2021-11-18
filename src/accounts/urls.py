from django.urls import path
from .views import CrossAuthView, IdentificationCheckView

app_name = "accounts"
urlpatterns = [
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth-view'),
    path('identification-check/', IdentificationCheckView.as_view(), name='identification-check'),
]
