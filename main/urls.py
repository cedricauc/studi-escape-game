from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scenario/<str:id>", views.details, name="details"),
    path("faq", views.faq, name="faq"),
    path("faq/<str:id>", views.faq, name="faq"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),
    path("manage", views.manage, name="manage"),
    path("chat", views.chat, name="chat"),
    path("booking", views.booking, name="booking")
]