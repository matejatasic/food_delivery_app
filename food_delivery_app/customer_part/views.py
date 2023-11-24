from django.core.exceptions import PermissionDenied
from django.forms import Form, ModelForm, ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm, LoginForm
from .services.login_service import LoginService
from .services.register_service import RegisterService


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/home.html")


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        login_service: LoginService = LoginService()
        form: Form = LoginForm(request.POST)

        try:
            login_service.login(request, form)

            return redirect(reverse("home"))
        except ValidationError:
            return render(request, "customer_part/login.html", {"form": form})
        except PermissionDenied:
            return render(request, "customer_part/login.html", {"form": form})

    return render(request, "customer_part/login.html", {"form": LoginForm()})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        register_service: RegisterService = RegisterService()
        form: ModelForm = RegisterForm(request.POST, request.FILES)

        try:
            register_service.register(form)

            return redirect(reverse("home"))
        except ValidationError:
            return render(request, "customer_part/register.html", {"form": form})

    return render(request, "customer_part/register.html", {"form": RegisterForm()})


def restaurant(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurant.html")


def restaurants(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurants.html")


def cart(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/cart.html")


def orders(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/orders.html")
