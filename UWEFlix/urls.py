from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register_user/", views.register, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("films/", views.FilmList.as_view()),
    path("films/<int:id>", views.FilmDetail.as_view()),
    path("screens/", views.ScreenList.as_view()),
    path("screens/<int:id>", views.ScreenDetail.as_view()),
    path("showings/", views.ShowingList.as_view()),
    path("showings/<int:id>", views.ShowingDetail.as_view()),
]

