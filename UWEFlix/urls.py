from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('customer', views.CustomerViewSet)
router.register('films', views.FilmViewSet)
router.register('screens', views.ScreenViewSet)
router.register('showings', views.ShowingViewSet)
router.register('booking', views.BookingViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-items', views.OrderItemViewSet)
# router.register('ticket', views.TicketViewSet)
# router.register('booking-item', views.BookingItemViewSet, basename='booking-item')

booking_router = routers.NestedDefaultRouter(router, 'booking', lookup='booking')
booking_router.register('items', views.BookingItemViewSet, basename='booking-items')

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register_user/", views.register, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path('', include(router.urls)),
    path('', include(booking_router.urls)),
]

