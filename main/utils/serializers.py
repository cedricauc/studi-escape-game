from rest_framework import serializers

from main.models import Booking, Game, GameDetails, ScenarioRoomClue


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = ['participant', 'is_canceled', 'game']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['start_time', 'end_time', 'scenario']


class GameDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameDetails
        fields = ['start_time', 'end_time', 'game', 'booking']


class ScenarioRoomClueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScenarioRoomClue
        fields = ['clue', 'scenario', 'room']
