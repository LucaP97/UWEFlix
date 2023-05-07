from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
router.register('account_manager', views.AccountManagerViewSet)
router.register('club_representative', views.ClubRepresentativeViewSet)
router.register('clubs', views.ClubViewSet)
# router.register('add_account', views.AddAccountViewSet)
router.register('accounts', views.AccountViewSet, basename='accounts')
router.register('discount-request', views.DiscountRequestViewSet, basename='discount-request')
router.register('club_booking', views.ClubBookingViewSet)
router.register('club_orders', views.ClubOrderViewSet, basename='club_orders')
router.register('club_order-items', views.ClubOrderItemViewSet)
router.register('archived_club_orders', views.ArchivedClubOrderViewSet, basename='archived_club_orders')
router.register('credit', views.CreditViewSet)
router.register('club_order_cancellation', views.ClubOrderCancellationViewSet, basename='club_order_cancellation')
# router.register('credit-item', views.CreditItemViewSet)

# accounts_router = routers.NestedDefaultRouter(router, 'accounts', lookup='account')
# accounts_router.register('statements', views.StatementsViewSet, basename='account-statement')

booking_router = routers.NestedDefaultRouter(router, 'club_booking', lookup='club_booking')
booking_router.register('club_items', views.ClubBookingItemViewSet, basename='club_booking-items')

urlpatterns = [
#     path("home/", views.home, name="home"),
#     path("login/", views.login_user, name="login"),
#     path("register_user/", views.register, name="register_user"),
#     path("logout_user/", views.logout_user, name="logout_user"),
    path('', include(router.urls)),
    path('', include(booking_router.urls)),
    # path('', include(accounts_router.urls)),
]
