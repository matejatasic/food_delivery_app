from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show/<str:id>", views.show, name="show"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("close/<str:id>", views.close, name="close"),
    path("comment", views.comment, name="comment"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
