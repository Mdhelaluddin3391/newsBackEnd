from django.urls import path
from .api import MeAPIView

urlpatterns = [
    path("me/", MeAPIView.as_view()),
]
