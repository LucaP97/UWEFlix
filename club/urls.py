from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('club_representative', views.ClubRepresentativeViewSet)
# router.register('films', views.FilmViewSet)
# router.register('screens', views.ScreenViewSet)
# router.register('showings', views.ShowingViewSet)

urlpatterns = [
#     path("home/", views.home, name="home"),
#     path("login/", views.login_user, name="login"),
#     path("register_user/", views.register, name="register_user"),
#     path("logout_user/", views.logout_user, name="logout_user"),
    path('', include(router.urls)),
]
