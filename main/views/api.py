from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from main.models import Scenario, Booking, Game, Discount, ScenarioRoomClue
from main.utils.serializers import BookingSerializer, GameSerializer, ScenarioRoomClueSerializer, \
    ScenarioSerializer
from main.utils.util import day_beginning, day_end, get_date


class IsParadoxEmployeePermission(permissions.BasePermission):
    message = "Vous devez être un employé de Paradox pour accéder à cette ressource."

    def has_permission(self, request, view):
        return request.user.role in [0, 1] or request.user.is_superuser


class ScenarioViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier des scénarios.
    """
    queryset = Scenario.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = ScenarioSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier des réservations.
    """
    queryset = Booking.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = BookingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        try:
            dt = self.request.query_params.get('dt')
            dt = datetime.strptime(dt, '%Y-%m-%d')
        except ValueError as ex:

            dt = None
        except TypeError as ex:
            dt = None

        return qs.filter(
            game__start_time__gt=day_beginning(dt),
            game__start_time__lt=day_end(dt)
        ).order_by("-game__start_time")

    def post(self, request, *args, **kwargs):
        # modifier une réservation
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier des séances.
    """
    queryset = Game.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = GameSerializer


class ScenarioRoomClueViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier les indices lors d'une partie
    """
    queryset = ScenarioRoomClue.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = ScenarioRoomClueSerializer
