from calendar import HTMLCalendar
from main.models import Game
from main.utils.util import exclude_booked_events


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, day=None, slug=None):
        self.year = year
        self.month = month
        self.day = day
        self.slug = slug
        super(Calendar, self).__init__()

    # formate un jour comme un td
    # filtrer les événements par jour
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)

        events_not_booked = exclude_booked_events(events_per_day)
        d = ''
        e = ''
        for event in events_per_day:
            d = f'bg-warning'

        for event in events_not_booked:
            d = f'bg-secondary'

        if day == self.day:
            e += f'active'

        if day != 0:
            return f"<td class='{d} {e}'><span class='dateD {e}'>{day}</span></td>"

        return '<td></td>'

    # formats par semaine comme un tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formate un mois sous forme de tableau
    # filtrer les événements par année et par mois
    def formatmonth(self, withyear=True):
        games = Game.objects.filter(start_time__year=self.year, start_time__month=self.month)
        if self.slug:
            games = games.filter(scenario__slug=self.slug)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, games)}\n'
        return cal
