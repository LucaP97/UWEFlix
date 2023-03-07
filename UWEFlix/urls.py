from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register_user/", views.register, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("films/", views.film_list)
]

