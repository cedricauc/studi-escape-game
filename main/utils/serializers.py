from rest_framework import serializers

from main.models import Scenario, Booking, Game, GameDetails, ScenarioRoomClue


class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scenario
        fields = ['title',
                  'description',
                  'duration',
                  'min_participant',
                  'max_participant',
                  'price_participant',
                  'slug']


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
