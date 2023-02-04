from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from .views import views, api, calendar

api_router = routers.DefaultRouter()
api_router.register(r"scenarios", api.ScenarioViewSet)
api_router.register(r"bookings", api.BookingViewSet)
api_router.register(r"games", api.GameViewSet)
api_router.register(r"clues", api.ScenarioRoomClueViewSet)

urlpatterns = [
    path("", views.HomeView, name='home'),
    path("login", views.LoginView, name="login_view"),
    path("register", views.RegisterView, name="register"),
    path("logout", views.LogoutView, name="logout"),
    path("profile", views.ManageProfileView, name="profile"),
    path("order", views.ManageOrderView, name="order"),
    path("scenario/<str:slug>", views.ScenarioView, name="scenario"),
    path("faq", views.FaqView, name="faq"),
    path("booking", views.BookingView, name="booking"),
    path("booking/sum", views.BookingSumView, name="booking_sum"),
    path("booking/final", views.BookingFinalView, name="booking_final"),
    path("booking/<str:slug>", views.BookingView, name="booking"),
    path("api/", include(api_router.urls)),
    path("api/calendar", calendar.CalendarViewSet, name="calendar_api"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)