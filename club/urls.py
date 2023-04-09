from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
router.register('club_representative', views.ClubRepresentativeViewSet)
router.register('clubs', views.ClubViewSet)
router.register('accounts', views.AccountViewSet)
router.register('booking', views.BookingViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-items', views.OrderItemViewSet)

# accounts_router = routers.NestedDefaultRouter(router, 'accounts', lookup='account')
# accounts_router.register('statements', views.StatementsViewSet, basename='account-statement')

booking_router = routers.NestedDefaultRouter(router, 'booking', lookup='booking')
booking_router.register('items', views.BookingItemViewSet, basename='booking-items')

urlpatterns = [
#     path("home/", views.home, name="home"),
#     path("login/", views.login_user, name="login"),
#     path("register_user/", views.register, name="register_user"),
#     path("logout_user/", views.logout_user, name="logout_user"),
    path('', include(router.urls)),
    path('', include(booking_router.urls)),
    # path('', include(accounts_router.urls)),
]
