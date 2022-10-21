from rest_framework import viewsets, permissions
from rest_framework.response import Response
from . import models
from .utils.serializers import BookingSerializer, GameSerializer, ScenarioRoomClueSerializer, \
    ScenarioSerializer
from .utils.util import day_beginning, day_end


class IsParadoxEmployeePermission(permissions.BasePermission):
    message = "Vous devez être un employé de Paradox pour accéder à cette ressource."

    def has_permission(self, request, view):
        return request.user.role in [0, 1] or request.user.is_superuser


class ScenarioViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier des scénarios.
    """
    queryset = models.Scenario.objects.all()
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
    queryset = models.Booking.objects.filter(
        game__start_time__gt=day_beginning(),
        game__start_time__lt=day_end()
    )

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = BookingSerializer

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
    queryset = models.Game.objects.all()
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
    queryset = models.ScenarioRoomClue.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = ScenarioRoomClueSerializer
