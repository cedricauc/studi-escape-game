from rest_framework import serializers
from main.models import Scenario, Booking, Game, ScenarioRoomClue


class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id',
                  'title',
                  'description',
                  'duration',
                  'min_participant',
                  'max_participant',
                  'price_participant',
                  'slug']


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    scenario_id = serializers.CharField(source='game.scenario.id')
    scenario_title = serializers.CharField(source='game.scenario.title')
    scenario_duration = serializers.CharField(source='game.scenario.duration')
    game_id = serializers.CharField(source='game.id')
    game_start_time = serializers.CharField(source='game.start_time')
    game_end_time = serializers.CharField(source='game.end_time')

    class Meta:
        model = Booking
        fields = ['id',
                  'participant',
                  'in_progress',
                  'is_complete',
                  'start_hour',
                  'start_minutes',
                  'end_hour',
                  'end_minutes',
                  'scenario_id',
                  'scenario_title',
                  'scenario_duration',
                  'game_id',
                  'game_start_time',
                  'game_end_time']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    scenario_id = serializers.CharField(source='scenario.id')
    scenario_title = serializers.CharField(source='scenario.title')

    class Meta:
        model = Game
        fields = ['id', 'start_time', 'end_time', 'scenario_id', 'scenario_title']


class ScenarioRoomClueSerializer(serializers.HyperlinkedModelSerializer):
    scenario_id = serializers.CharField(source='scenario.id')
    scenario_title = serializers.CharField(source='scenario.title')
    room_num = serializers.CharField(source='room.num')

    class Meta:
        model = ScenarioRoomClue
        fields = ['clue', 'scenario_id', 'scenario_title', 'room_num']
