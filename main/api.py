from rest_framework import viewsets, permissions
from . import models
from .utils.serializers import BookingSerializer, GameSerializer, GameDetailsSerializer, ScenarioRoomClueSerializer, \
    ScenarioSerializer


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
    queryset = models.Booking.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = BookingSerializer


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


class GameDetailsViewSet(viewsets.ModelViewSet):
    """
    API qui permet d'afficher ou de modifier le détails des séances.
    """
    queryset = models.GameDetails.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsParadoxEmployeePermission,
    ]
    serializer_class = GameDetailsSerializer


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
