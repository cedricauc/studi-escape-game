from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from main.forms import RegisterForm, ManageForm, ChatForm, BookingForm
from main.models import User, Scenario, GameDetails, TicketAnswer, TicketCategory, TicketQuestion, Booking, Discount, \
    Cart

from datetime import datetime, date

from main.utils.util import prepare_booking, create_booking_number


def home(request):
    scenarios = Scenario.objects.all()
    discounts = Discount.objects.all()
    context = {
        "scenarios": scenarios,
        "discounts": discounts
    }

    return render(request, "main/index.html", context)


def scenario(request, slug):
    # requête pour le scénario demandé
    if not slug:
        data = Scenario.objects.all().first()
    else:
        data = Scenario.objects.get(slug=slug)

    record_time = None
    try:
        # pour chaque partie terminée du scénario ci-dessus
        for itr in data.games.all():
            row = GameDetails.objects.get(game=itr)
            # calcul en delta time de la différence début/fin partie
            diff_dt = datetime.combine(date.today(), row.end_time) - datetime.combine(date.today(), row.start_time)
            diff = diff_dt.total_seconds() / 3600
            # si e temps est inférieur alors stocker dans la variable record_time
            if diff < record_time:
                record_time = diff
    except GameDetails.DoesNotExist:
        record_time = None

    context = {
        "scenario": data,
        "record_time": record_time
    }

    return render(request, "main/scenario.html", context)


def faq(request, slug=None):
    if not slug:
        category = TicketCategory.objects.all().first()
    else:
        category = TicketCategory.objects.get(slug=slug)

    data = TicketAnswer.objects.filter(question__category=category).order_by("id")

    context = {
        "data": data,
        "category": category,
        "categories": TicketCategory.objects.all()
    }

    return render(request, "main/faq.html", context)


@csrf_exempt
def login_view(request):
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
                "message": "Invalide e-mail/mot de passe"
            })

    context = {
        'next': request.GET.get('next')
    }
    return render(request, "main/login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
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
                return render(request, "main/register.html", context)

            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context = {
                'form': form
            }
            return render(request, "main/register.html", context)
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, "main/register.html", context)


@login_required(login_url="login_view")
def order(request):
    data = Booking.objects.all()

    context = {
        "data": data,
        "template": "order"
    }

    return render(request, "main/order.html", context)


@login_required(login_url="login_view")
def manage(request):
    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = ManageForm(request.POST)
        # Vérifiez s'il est valide :
        if form.is_valid():
            # traiter les données
            user = form.save(commit=False)
            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.save()

            return HttpResponseRedirect('/manage')
    else:
        # Créer une instance de formulaire et la remplir avec les données initiales
        form = ManageForm(
            initial={'id': request.user.id, 'first_name': request.user.first_name, 'last_name': request.user.last_name})

    context = {
        "form": form,
        "template": "manage"
    }

    return render(request, "main/manage.html", context)


@login_required(login_url="login_view")
def chat(request):
    if request.method == "POST":
        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = ChatForm(request.POST)
        # Vérifiez s'il est valide :
        if form.is_valid():
            # traiter les données
            category = TicketCategory.objects.get(title=request.POST.get("category"))
            question = request.POST.get("question")
            ticket_question = TicketQuestion(author=request.user.username, category=category, question=question)
            ticket_question.save()

            return render(request, "main/chat.html", {
                "form": form,
                "template": "chat",
                "success": "Question bien transmis"
            })
    else:
        # Créer une instance de formulaire
        form = ChatForm()

    context = {
        "form": form,
        "template": "chat"
    }

    return render(request, "main/chat.html", context)


def booking(request, slug=None):
    if request.method == "POST":

        # Créez une instance de formulaire et remplissez-la avec les données de la requête :
        form = BookingForm(request.POST)
        # Ajouter les donnes de l'api scénario et horaires séances au choix des champs de sélection
        s = request.POST.get("scenario")
        form.fields['scenario'].choices = [(s, s)]
        start_time = request.POST.get("start_time")
        form.fields['start_time'].choices = [(start_time, start_time)]
        # Vérifiez s'il est valide :
        if form.is_valid():
            cart = Cart(game_id=start_time, participant=request.POST.get("participant"))
            cart.save()
            request.session['cart'] = cart.id
            return HttpResponseRedirect(reverse("booking_sum"))
    form = BookingForm()

    context = {
        "form": form,
    }
    return render(request, "main/booking.html", context)


@login_required(login_url="login_view")
def booking_sum(request):
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
def booking_final(request):
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
