from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import Form, ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import anonimity_required
from .forms import RegisterForm, LoginForm
from .services.address_service import AddressService
from .services.login_service import LoginService
from .services.register_service import RegisterService


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/home.html")


@anonimity_required("home")
def login(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
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


@anonimity_required("home")
def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        register_service: RegisterService = RegisterService()
        form: ModelForm = RegisterForm(request.POST, request.FILES)

        try:
            register_service.register(request, form)

            return redirect(reverse("home"))
        except ValidationError:
            return render(request, "customer_part/register.html", {"form": form})

    return render(request, "customer_part/register.html", {"form": RegisterForm()})


@login_required
def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)

    return redirect(reverse("home"))


def restaurant(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurant.html")


def restaurants(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/restaurants.html")


def cart(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/cart.html")


def orders(request: HttpRequest) -> HttpResponse:
    return render(request, "customer_part/orders.html")


def addresses(request: HttpRequest):
    address_service = AddressService()
    addresses: list[dict[str, str]] = address_service.get_address_options(
        request.GET["term"]
    )

    return JsonResponse(
        {
            "results": addresses,
        },
        encoder=DjangoJSONEncoder,
    )
