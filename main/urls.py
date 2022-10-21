from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from . import api
from .views import views, calendar

api_router = routers.DefaultRouter()
api_router.register(r"scenarios", api.ScenarioViewSet)
api_router.register(r"bookings", api.BookingViewSet)
api_router.register(r"games", api.GameViewSet)
api_router.register(r"clues", api.ScenarioRoomClueViewSet)

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", include(api_router.urls)),
    path("scenario/<str:slug>", views.scenario, name="scenario"),
    path("faq", views.faq, name="faq"),
    path("faq/<str:slug>", views.faq, name="faq"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),
    path("manage", views.manage, name="manage"),
    path("chat", views.chat, name="chat"),
    path("booking/sum", views.booking_sum, name="booking_sum"),
    path("booking/final", views.booking_final, name="booking_final"),
    path("booking", views.booking, name="booking"),
    path("booking/<str:slug>", views.booking, name="booking"),
    path("api/calendar", calendar.calendar, name="calendar_api"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
