import calendar
from django.db.models import Q
from main.models import Scenario, Cart, Discount, Booking
from datetime import datetime, date, timedelta


def footer_scenario(request):
    """
    Retourne liste des scénarios
    """
    return {'footer_scenario': Scenario.objects.all()}


def prepare_booking(cart_id):
    """
    Retourne une liste de variables pour finaliser une réservation
    """
    cart = Cart.objects.get(pk=cart_id)

    discounts = Discount.objects.filter(scenarios__games__cart__exact=cart)

    total = cart.game.scenario.price_participant * cart.participant
    discount = 0
    for row in discounts.order_by("-discount"):
        if cart.participant >= row.step:
            if row.is_percentage:
                discount = round((total * (row.discount / 100)), 2)
            else:
                discount = row.discount
            break
    total_amount = total - discount

    return [cart, discount, total, total_amount]


def create_booking_number(scenario_title):
    """
    Retourne une chaîne de caractère correspondant à un identifiant de réservation
    """
    today = date.today()
    first_letters = "".join(word[0].upper() for word in scenario_title.split())
    return first_letters + today.strftime("%d%m%Y%H%M")


def get_date(req_day):
    """
    Retoure la date du jour
    """
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.today()


def prev_month(d):
    """
    Retourne la date du mois précédent
    """
    first = d.replace(day=1)
    month = first - timedelta(days=1)
    return month


def next_month(d):
    """
    Retourne la date du mois prochain
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    month = last + timedelta(days=1)
    return month


def exclude_booked_events(events):
    """
    Exclure les séances réservées
    """
    # Bloquer les séances ajoutées à un panier pour une durée de 5 minutes
    carts = []
    for cart in Cart.objects.all():
        if not cart.created_date + timedelta(minutes=5) < datetime.now():
            carts.append(cart.id)

    events = events.exclude(
        Q(id__in=Booking.objects.filter(is_canceled=False).values_list('game_id', flat=True).all()) |
        Q(id__in=carts)
    )

    return events


def day_beginning(dt=None):
    """
    Retourne le début de la journée
    """
    if not dt:
        dt = get_date(None)

    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def day_end(dt=None):
    """
    Retourne la fin de la journée
    """
    if not dt:
        dt = get_date(None)

    return dt.replace(hour=23, minute=59, second=0, microsecond=0)


def time_conversion(sec):
    """
    Conversion de secondes en heures et minutes
    """
    sec_value = sec % (24 * 3600)
    hour_value = sec_value // 3600
    sec_value %= 3600
    min_value = sec_value // 60
    sec_value %= 60
    return {hour_value, min_value}
