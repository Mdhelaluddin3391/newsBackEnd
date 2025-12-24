from django.urls import path
from .api import SearchAPIView

urlpatterns = [
    path("", SearchAPIView.as_view()),
]
