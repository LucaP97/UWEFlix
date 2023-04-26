from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
# router.register('orders', views.OrderViewSet, basename='orders')
# router.register('accounts', views.AccountViewSet, basename='accounts')
# router.register('uweflix-statement-items', views.UweflixStatementItemsViewSet, basename='uweflix-statement-items')
router.register('statements', views.StatementViewSet, basename='statements')
# router.register('statements', views.StatementViewSet, basename='statements')


# booking_router = routers.NestedDefaultRouter(router, 'booking', lookup='booking')
# booking_router.register('items', views.BookingItemViewSet, basename='booking-items')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(booking_router.urls)),
]
