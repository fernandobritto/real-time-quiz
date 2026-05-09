"""URL configuration for the web (template) layer."""
from django.urls import path

from web import views

app_name = "web"

urlpatterns = [
    path("", views.IndexRedirectView.as_view(), name="index"),
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("quiz/result/", views.ResultView.as_view(), name="result"),
    path("quiz/restart/", views.RestartView.as_view(), name="restart"),
]
