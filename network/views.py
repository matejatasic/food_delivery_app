import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like
from .forms import PostForm


DEFAULT_ITEMS_PER_PAGE = 10


def index(request):
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, DEFAULT_ITEMS_PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template_parameters = {
        "form": PostForm(),
        "posts": page_obj
    }
    # sredi logiku za prikazivanje ikonice na index.html kad je svidjano ili ne
    if request.user.is_authenticated:
        likes = list(request.user.likes.all())
        likes_ids = map(lambda l: int(l.post.id), likes)
        likes_ids = list(likes_ids)
        template_parameters["posts_liked"] = likes_ids

    return render(request, "network/index.html", template_parameters)


def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if not form.is_valid():
            return render(request, "network/index.html", {
                "form": form
            })
        
        Post.objects.create(content=form.cleaned_data["content"], user=request.user)

        return redirect(reverse("index"))


def profile(request, id):
    template_parameters = {}

    try:
        user = User.objects.get(id=id)
        posts = user.posts.all().order_by("-created")

        template_parameters["requested_user"] = user
        paginator = Paginator(posts, DEFAULT_ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        template_parameters["posts"] = page_obj
    except:
        return render(request, "network/error.html", {
            "title": "Invalid user",
            "message": f"The user with the id {id} does not exist"
        })

    if request.user.is_authenticated and request.user.id != user.id:
        try:
            user.follows_from.get(user_following_id=request.user.id)
            template_parameters["is_following"] = True
        except:
            template_parameters["is_following"] = False

    return render(request, "network/profile.html", template_parameters)


@csrf_exempt
def edit(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return JsonResponse({"error": f"The user with the id {id} does not exis"}, status=400)

    if post.user.id != request.user.id:
        return JsonResponse({"error": f"You are not authorized to edit this post"}, status=400)

    if request.method == "POST":
        data = json.loads(request.body)
        post.content = data.get("content")
        post.save()

        return JsonResponse({"message": "Post successfully edited"}, status=200)


@login_required
def follow(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id", 0)

        try:
            user = User.objects.get(id=user_id)
        except:
            return render(request, "network/error.html", {
                "title": "Invalid user",
                "message": f"The user with the id {user_id} does not exist"
            })
        
        try:
            follow = user.follows_from.get(user_following_id=request.user.id, user_followed_id=user_id)
            follow.delete()
        except: 
           Follow.objects.create(user_following=request.user, user_followed=user)


        return redirect(reverse("profile", args=[user_id]))
    

@csrf_exempt
@login_required
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except:
            return JsonResponse({"error": f"The post with the id {post_id} does not exis"}, status=400)

        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            action = "unliked"
        except:
            Like.objects.create(post=post, user=request.user)
            action = "liked"

        return JsonResponse({"message": f"The post was {action}", "action": action, "current_number_of_likes": post.likes.count()}, status=200)


@login_required
def following(request):
    follows = request.user.follows_to.all()

    posts_by_users = map(lambda f: list(f.user_followed.posts.all()), follows)
    posts_by_users = list(posts_by_users)
    posts = []
    
    for posts_by_user in posts_by_users:
        for post in posts_by_user:
            posts.append(post)

    paginator = Paginator(posts, DEFAULT_ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "posts": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
