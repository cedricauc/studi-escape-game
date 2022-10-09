from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ManageForm, ChatForm
from .models import User, Scenario, Game, GameDetails, TicketAnswer, TicketCategory, TicketQuestion, Booking

from datetime import datetime, date


def home(request):
    return render(request, "main/index.html")


def scenario(request, slug):
    # requête pour le scénario demandé
    try:
        data = Scenario.objects.get(slug=slug)
    except Scenario.DoesNotExist:
        data = Scenario.objects.all().first()

    record_time = data.duration
    # pour chaque partie terminée du scénario ci-dessus
    for itr in data.games.all():
        row = GameDetails.objects.get(game=itr)
        # calcul en delta time de la différence début/fin partie
        diff_dt = datetime.combine(date.today(), row.end_time) - datetime.combine(date.today(), row.start_time)
        diff = diff_dt.total_seconds() / 3600
        # si e temps est inférieur alors stocker dans la variable record_time
        if diff < record_time:
            record_time = diff

    context = {
        "scenario": data,
        "record_time": record_time
    }

    return render(request, "main/scenario.html", context)


def faq(request, id=None):
    if id:
        category = TicketCategory.objects.get(pk=id)
    else:
        category = TicketCategory.objects.all().first()

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalide e-mail/mot de passe"
            })
    return render(request, "main/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
                user.save()
            except IntegrityError:
                context = {
                    'form': form
                }
                return render(request, "main/register.html", context)

            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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


@login_required(login_url="login")
def order(request):
    data = Booking.objects.all()

    context = {
        "data": data,
        "template": "order"
    }

    return render(request, "main/order.html", context)


@login_required(login_url="login")
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
        # Create a form instance and populate it with initial data
        form = ManageForm(
            initial={'id': request.user.id, 'first_name': request.user.first_name, 'last_name': request.user.last_name})

    context = {
        "form": form,
        "template": "manage"
    }

    return render(request, "main/manage.html", context)


@login_required(login_url="login")
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
        # Create a form instance and populate it with initial data
        form = ChatForm()

    context = {
        "form": form,
        "template": "chat"
    }

    return render(request, "main/chat.html", context)


def booking(request):
    return render(request, "main/booking.html")
