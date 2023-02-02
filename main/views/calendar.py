from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

    rows = Game.objects.filter(start_time__year=date.year,
                               start_time__month=date.month,
                               start_time__day=date.day)

    rows = exclude_booked_events(rows)

    slug = None
    if request.GET.get('scenario') and request.GET.get('scenario') != "booking":
        slug = request.GET.get('scenario')
        rows = rows.filter(scenario__slug=slug)

    scenarios = Scenario.objects.filter(games__in=rows.all())

    data = []

    for scenario in scenarios:
        data.append({
            'id': scenario.id,
            'title': scenario.title,
            'price': scenario.price_participant,
            'min_participant': scenario.min_participant,
            'max_participant': scenario.max_participant,
            'start_time': list(
                rows.filter(scenario=scenario).all().values('id', 'start_time', 'scenario_id'))
        })

    # Instancier notre classe de calendrier avec l'année et la date d'aujourd'hui
    cal = Calendar(date.year, date.month, date.day, slug)

    # Appelez la méthode formatmonth, qui renvoie notre calendrier sous forme de tableau
    html_cal = cal.formatmonth(withyear=True)
    context = {
        "calendar": mark_safe(html_cal),

    }
    # Rendre le modèle HTML en texte
    html = render_to_string("calendar/calendar.html", context)

    return JsonResponse({
        "content": html,
        "data": data,
        "date": date
    })
