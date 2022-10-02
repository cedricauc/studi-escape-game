from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scenario/<str:id>", views.details, name="details"),
]