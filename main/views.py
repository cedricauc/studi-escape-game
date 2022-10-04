from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")


def details(request, id):
    return render(request, "main/details.html")


def faq(request, id=''):
    return render(request, "main/faq.html")


def login(request):
    return render(request, "main/login.html")


def register(request):
    return render(request, "main/register.html")
