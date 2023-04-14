from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
# router.register('orders', views.UweflixAccountsViewSet)
# router.register('statements', views.StatementViewSet)


# booking_router = routers.NestedDefaultRouter(router, 'booking', lookup='booking')
# booking_router.register('items', views.BookingItemViewSet, basename='booking-items')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(booking_router.urls)),
]
