from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")


def details(request, id):
    return render(request, "main/details.html")
