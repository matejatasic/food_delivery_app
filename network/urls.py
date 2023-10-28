from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit/<str:id>", views.edit, name="edit"),
    path("profile/<str:id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name="like"),
    path("following", views.following,name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
