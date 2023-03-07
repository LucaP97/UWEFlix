from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register_user/", views.register, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("films/", views.film_list),
    path("films/<int:id>", views.film_detail),
    path("screens/", views.screen_list),
    path("screens/<int:id>", views.screen_detail),
    path("showings/", views.showing_list),
    path("showings/<int:id>", views.showing_detail),
]

