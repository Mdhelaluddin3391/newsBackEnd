from django.urls import path
from .api import ToggleReactionAPIView

urlpatterns = [
    path("toggle/", ToggleReactionAPIView.as_view()),
]
