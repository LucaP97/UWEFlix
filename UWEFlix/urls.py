from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('films', views.FilmViewSet)
router.register('screens', views.ScreenViewSet)
router.register('showings', views.ShowingViewSet)

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register_user/", views.register, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("showings/booking/<int:id>", views.booking_request, name="booking_request"),
    path('', include(router.urls)),
]

