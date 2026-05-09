"""URL configuration for the API layer."""
from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("question/<int:index>/", views.QuestionView.as_view(), name="question"),
    path("answer/", views.AnswerView.as_view(), name="answer"),
]
