from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Listing, User, Bid, Comment, Category
from .forms import ListingCreateForm


def index(request):
    listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def show(request, id):
    listing = None
    latest_price = None

    try:
        listing = Listing.objects.get(id=id)
    except:
        return render(request, "auctions/error.html", {
            "title": "Listing not found",
            "message": f"The listing with the id {id} does not exist"
        })

    try:
        latest_price = listing.bids.all().order_by("-amount").first().amount
    except:
        latest_price = listing.starting_price

    template_parameters = {
        "listing": listing,
        "latest_price": latest_price
    }

    if request.user.is_authenticated:
        try:
            is_listing_in_watchlist = request.user.watchlist.get(id=id) != None
            template_parameters["is_listing_in_watchlist"] = is_listing_in_watchlist
        except:
            template_parameters["is_listing_in_watchlist"] = False
    
    if not listing.is_active:
        winner = listing.bids.all().order_by("-amount").first().user
        template_parameters["is_closed"] = True
        template_parameters["winner"] = winner

    return render(request, "auctions/show.html", template_parameters)

@login_required
def watchlist(request):
    if request.method == "POST":
        action = request.POST.get("action", None)
        listing_id = request.POST.get("listing_id", None)
        listing = None
        valid_actions = ("add", "remove")

        if not action in valid_actions:
            return render(request, "auctions/error.html", {
                "title": "Invalid action",
                "message": f"The action {action} is not a valid action"
            })
        
        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            listing = None
        
        if action == "add":
            request.user.watchlist.add(listing)

            return redirect(reverse("show", args=[listing_id]))
        
        request.user.watchlist.remove(listing)

        return redirect(reverse("show", args=[listing_id]))
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })
    
@login_required
def bid(request, id):
    if request.method == "POST":
        listing = None

        try:
            listing = Listing.objects.get(id=id)
        except:
            return render(request, "auctions/error.html", {
                "title": "Listing not found",
                "message": f"The listing with the id {id} does not exist"
            })
        
        bid_amount = request.POST.get("bid_amount", "0")
        bid_amount = int(bid_amount)

        try:
            latest_price = listing.bids.all().order_by("-amount").first().amount
        except:
            latest_price = listing.starting_price
        
        if  bid_amount < listing.starting_price or bid_amount <= latest_price:
            return render(request, "auctions/error.html", {
                "title": "Bid too small",
                "message": f"The bid should be bigger than {latest_price} to be accepted"
            })

        Bid.objects.create(amount=bid_amount, listing=listing, user=request.user)

        return redirect(reverse("show", args=[listing.id]))
    
@login_required
def close(request, id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(id=id)
        except:
            return render(request, "auctions/error.html", {
                "title": "Listing not found",
                "message": f"The listing with the id {id} does not exist"
            })
        
        if request.user.username != listing.creator.username:
            return render(request, "auctions/error.html", {
                "title": "Not authorized",
                "message": f"You are not authorized to close this listing"
            })
        
        if not listing.is_active:
            return render(request, "auctions/error.html", {
                "title": "Alredy closed",
                "message": f"This listing is already closed"
            })

        listing.is_active = False
        listing.save()

        return redirect(reverse("show", args=[listing.id]))
    
@login_required
def comment(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id", 0)

        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            return render(request, "auctions/error.html", {
                "title": "Listing not found",
                "message": f"The listing with the id {listing_id} does not exist"
            })
        
        comment = request.POST.get("comment", "").strip()

        if comment == "":
            return render(request, "auctions/error.html", {
                "title": "Empty Comment",
                "message": f"The comment cannot be empty"
            })

        Comment.objects.create(
            comment=comment,
            user=request.user,
            listing=listing
        )

        return redirect(reverse("show", args=[listing.id]))

@login_required
def create(request):
    if request.method == "POST":
        form = ListingCreateForm(request.POST)

        if not form.is_valid():
            return render(request, "auctions/create.html", {
                "form": form
            })
        
        Listing.objects.create(
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            starting_price=form.cleaned_data["starting_price"],
            category=form.cleaned_data["category"],
            image=form.cleaned_data["image"],
            creator=request.user
        )

        return redirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": ListingCreateForm()
    })

def categories(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_id = request.POST.get("category_id", 0)
        
        try:
            category = Category.objects.get(id=category_id)
        except:
            return render(request, "auctions/error.html", {
                "title": "Category not found",
                "message": f"The category with the id {category_id} does not exist"
            })

        return render(request, "auctions/categories.html", {
            "selected_category": category.title,
            "listings": category.listings.filter(is_active=True),
            "categories": categories
        })

    return render(request, "auctions/categories.html", {
        "categories": categories
    })