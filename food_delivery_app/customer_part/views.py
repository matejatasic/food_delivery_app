from django.forms import ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm
from .services import RegisterService


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/home.html")


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/login.html")


def register(request: HttpRequest) -> HttpResponse:
    form = RegisterForm()
    register_service = RegisterService()

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        register_service.register(form)
        try:
            # register_service.register(form)

            return redirect(reverse("home"))
        except ValidationError:
            pass

    return render(request, "customer_part/register.html", {"form": form})


def restaurant(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurant.html")


def restaurants(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurants.html")


def cart(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/cart.html")


def orders(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/orders.html")
