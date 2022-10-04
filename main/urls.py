from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scenario/<str:id>", views.details, name="details"),
    path("faq", views.faq, name="faq"),
    path("faq/<str:id>", views.faq, name="faq"),
    path("login", views.login, name="login")
]