from django.db import IntegrityError
from django.db.models import Min, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.forms import RegisterForm, BookingForm, ManageProfileForm, FaqForm
from main.models import User, Scenario, TicketAnswer, TicketCategory, TicketQuestion, Booking, Discount, \
    Cart
from datetime import datetime, date
from main.utils.util import prepare_booking, create_booking_number, time_conversion


def HomeView(request):
    """
    Rend la page d'accueil avec tous les scénarios et informations associés
    """

    scenarios = Scenario.objects.all()
    discounts = Discount.objects.all()

    min_participant = Scenario.objects.aggregate(Min('min_participant'))
    max_participant = Scenario.objects.aggregate(Max('max_participant'))

    ticket_items = TicketAnswer.objects.order_by('-question__category', '-created_date')

    context = {
        "scenarios": scenarios,
        "discounts": discounts,
        "min_participant": min_participant,
        "max_participant": max_participant,
        "ticket_items": ticket_items
    }

    return render(request, "main/index.html", context)


@csrf_exempt
def LoginView(request):
    """
    Conexion utilisateur
    """
    if request.method == "POST":
        # authentifier un utilisateur
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # authentification réussie
        if user is not None:
            login(request, user)

            redirect_to_page = request.POST.get('next')
            if redirect_to_page != 'None':
                return redirect(redirect_to_page)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", {
                'message': "Invalide e-mail/mot de passe",
                'next': request.GET.get('next'),
                'form': RegisterForm()
            })

    # rediriger vers url initiale
    context = {
        'next': request.GET.get('next'),
        'form': RegisterForm()
    }
    return render(request, "main/login.html", context)


def RegisterView(request):
    """
    Inscription utilisateur
    """
    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = RegisterForm(request.POST)
        # Vérifiez s'il est valide :
        if form.is_valid():
            try:
                user_form = form.save(commit=False)
                # créer un utilisateur
                user = User.objects.create_user(user_form.email, user_form.email, user_form.password)
                user.last_name = user_form.last_name
                user.first_name = user_form.first_name
                # définir un role client à l'utilisateur
                user.role = 2
                user.save()
            except IntegrityError:
                context = {
                    'form': form
                }
                return render(request, "main/login.html", context)

            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context = {
                'form': form
            }
            return render(request, "main/login.html", context)
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, "main/login.html", context)


def LogoutView(request):
    """
    Deconexion utilisateur
    """
    logout(request)
    return HttpResponseRedirect(reverse("home"))


@login_required(login_url="login_view")
def ManageProfileView(request):
    """
    Gestion utilisateur
    """
    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = ManageProfileForm(request.POST)
        # Vérifiez s'il est valide :
        if form.is_valid():
            # traiter les données
            user = form.save(commit=False)
            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.save()

            return HttpResponseRedirect('/profile')
    else:
        # Créer une instance de formulaire et la remplir avec les données initiales
        form = ManageProfileForm(
            initial={'id': request.user.id, 'first_name': request.user.first_name, 'last_name': request.user.last_name})

    context = {
        "form": form,
        "template": "profile"
    }

    return render(request, "main/profile.html", context)


@login_required(login_url="login_view")
def ManageOrderView(request):
    """
    Gestion des commandes
    """
    data = Booking.objects.all()

    context = {
        "data": data,
        "template": "order"
    }

    return render(request, "main/order.html", context)


def ScenarioView(request, slug):
    """
    Rend la page d'un scénario avec les informations associés
    """
    # si scenario passé dans l'url de la requête
    if not slug:
        data = Scenario.objects.all().first()
    else:
        data = Scenario.objects.get(slug=slug)

    record_time = None
    now = datetime.now()

    # pour chaque partie terminée du scénario ci-dessus
    for itr in data.games.all():
        try:
            row = Booking.objects.get(game=itr, is_complete=True)
            start = now.replace(hour=row.start_hour, minute=row.start_minutes)
            end = now.replace(hour=row.end_hour, minute=row.end_minutes)
            # calcul en delta time de la différence début/fin partie
            diff_dt = datetime.combine(date.today(), end.time()) - datetime.combine(date.today(), start.time())
            diff = diff_dt.total_seconds()
            # si le temps est inférieur alors stocker dans la variable record_time
            if record_time is None or diff < record_time:
                record_time = diff
        except Booking.DoesNotExist:
            row = None

    hour_value, min_value = time_conversion(record_time) if record_time else [0, 0]

    context = {
        "scenario": data,
        "hour_value": hour_value,
        "min_value": min_value
    }

    return render(request, "main/scenario.html", context)


def FaqView(request):
    """
    Rend la page de la FAQ avec toutes catégories de questions
    """
    ticket_items = TicketAnswer.objects.order_by('-question__category', '-created_date')

    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = FaqForm(request.POST)
        # Vérifiez s'il est valide :
        if form.is_valid():
            # traiter les données
            author = request.POST.get("author")
            category = TicketCategory.objects.get(title=request.POST.get("category"))
            question = request.POST.get("question")
            ticket_question = TicketQuestion(author=author, category=category, question=question)
            ticket_question.save()

            return render(request, "main/faq.html", {
                "ticket_items": ticket_items,
                "form": form,
                "success": "Question envoyé"
            })
    else:
        # Créer une instance de formulaire
        form = FaqForm()

    context = {
        "form": form,
        "ticket_items": ticket_items
    }

    return render(request, "main/faq.html", context)


def BookingView(request, slug=None):
    """
    Rend la page de la de réservations d'une séance
    """
    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = BookingForm(request.POST)
        # Ajouter les donnes de l'api scénario et horaires séances au choix des champs de sélection
        form.fields['scenario'].choices = [(request.POST.get("scenario"), request.POST.get("scenario"))]
        form.fields['start_time'].choices = [(request.POST.get("start_time"), request.POST.get("start_time"))]
        # Vérifiez s'il est valide :
        if form.is_valid():
            cart = Cart(game_id=request.POST.get("start_time"), participant=request.POST.get("participant"))
            cart.save()
            request.session['cart'] = cart.id
            return HttpResponseRedirect(reverse("booking_sum"))
    form = BookingForm()

    context = {
        "form": form,
    }
    return render(request, "main/booking.html", context)


@login_required(login_url="login_view")
def BookingSumView(request):
    """
    Rend la page du panier des réservations
    """
    if "cart" not in request.session:
        context = {
            "empty_cart": True
        }
        return render(request, "main/booking_sum.html", context)

    if request.method == "POST":
        if "update" in request.POST:
            if request.POST.get("remove_from_cart"):
                Cart.objects.filter(pk=request.session['cart']).delete()
                # supprime session cart
                del request.session["cart"]
                context = {
                    "empty_cart": True
                }
                return render(request, "main/booking_sum.html", context)

        if "checkout" in request.POST:
            return HttpResponseRedirect(reverse("booking_final"))

    cart, discount, total, total_amount = prepare_booking(request.session['cart'])

    context = {
        "cart": cart,
        "scenario": cart.game.scenario,
        "discount": discount,
        "total": total,
        "total_amount": total_amount
    }
    return render(request, "main/booking_sum.html", context)


@login_required(login_url="login_view")
def BookingFinalView(request):
    """
    Rend la page de validation du panier des réservations
    """
    if "cart" not in request.session:
        return HttpResponseRedirect(reverse("booking"))

    if request.method == "POST":
        if request.POST.get("tos"):
            cart, discount, total, total_amount = prepare_booking(request.session['cart'])

            booker = Booking(
                booking_number=create_booking_number(cart.game.scenario.title),
                participant=cart.participant,
                total_amount=total_amount,
                game=cart.game,
                user=request.user)
            booker.save()

            Cart.objects.filter(pk=request.session['cart']).delete()
            # supprime session cart
            del request.session["cart"]

            return HttpResponseRedirect(reverse("order"))

    return render(request, "main/booking_final.html", {})
