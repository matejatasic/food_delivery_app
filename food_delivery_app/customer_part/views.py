from django.shortcuts import render


def index(request):
    return render(request, "customer_part/home.html")

def login(request):
    return render(request, "customer_part/login.html")

def register(request):
    return render(request, "customer_part/register.html")