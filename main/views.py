from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from main.forms import RegisterForm
from main.models import User


def index(request):
    return render(request, "main/index.html")


def details(request, id):
    return render(request, "main/details.html")


def faq(request, id=''):
    return render(request, "main/faq.html")


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
            context= {
                'form': form
            }
            return render(request, "main/register.html", context)
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, "main/register.html", context)


def order(request):
    return render(request, "main/order.html")


def manage(request):
    return render(request, "main/manage.html")


def chat(request):
    return render(request, "main/chat.html")


def booking(request):
    return render(request, "main/booking.html")
