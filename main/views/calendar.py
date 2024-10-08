import json
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from main.utils.calendar import Calendar
from main.utils.util import get_date, next_month, prev_month, exclude_booked_events
from main.models import Game, Scenario


@csrf_exempt
def CalendarViewSet(request):
    date = get_date(request.GET.get('day', None))

    if request.GET.get('nav') == "next_month":
        date = next_month(date)
    elif request.GET.get('nav') == "prev_month":
        date = prev_month(date)

    # Filtre la liste des séances à une date précise
    games = Game.objects.filter(start_time__year=date.year,
                                start_time__month=date.month,
                                start_time__day=date.day)

    # Retire les séances déjà réservées
    games = exclude_booked_events(games)

    # Filtre les séances avec le paramètre slug passé dans l'URL
    slug = None
    if request.GET.get('scenario') and request.GET.get('scenario') != "booking":
        slug = request.GET.get('scenario')
        games = games.filter(scenario__slug=slug)

    # Récupére la liste distincte des scénarios pour les séances a la date sélectionnée
    scenarios = Scenario.objects.distinct("title").filter(games__in=games.all())

    # Pour chaque scénario, ajouter la liste des séances
    data = []
    for scenario in scenarios:
        filtered_games = []
        for row in games.filter(scenario=scenario).all().values('id', 'start_time', 'scenario_id'):
            filtered_games.append({
                'id': row['id'],
                'start_time': row['start_time'].strftime('%Y-%m-%d %H:%M'),
                'scenario_id': row['scenario_id']
            })
        data.append({
            'id': scenario.id,
            'title': scenario.title,
            'price': str(scenario.price_participant),
            'min_participant': scenario.min_participant,
            'max_participant': scenario.max_participant,
            'start_time': filtered_games
        })

    # Instancier notre classe de calendrier avec l'année et la date d'aujourd'hui
    cal = Calendar(date.year, date.month, date.day, slug)

    # Appelez la méthode formatmonth, qui renvoie notre calendrier sous forme de tableau
    html_cal = cal.formatmonth(withyear=True)

    response = {
        "content": mark_safe(html_cal),
        "data": json.dumps(data),
        "date": date.strftime('%Y-%m-%d')
    }
    dump = json.dumps(response)
    return HttpResponse(dump, content_type='application/json')
