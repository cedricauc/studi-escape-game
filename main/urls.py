from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("scenario/<str:slug>", views.scenario, name="scenario"),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
