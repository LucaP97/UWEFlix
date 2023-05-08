from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('student', views.StudentViewSet, basename='student')
router.register('cinema-manager', views.CinemaManagerViewSet)
router.register('employee', views.EmployeeViewSet)
router.register('temporary-cinema-manager', views.TemporaryCinemaManagerViewSet)
router.register('films', views.FilmViewSet)
router.register('archived-films', views.ArchivedFilmViewSet, basename='archived-films')
router.register('screens', views.ScreenViewSet)
router.register('showings', views.ShowingViewSet)
router.register('booking', views.BookingViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-items', views.OrderItemViewSet)
router.register('prices', views.PriceViewSet)
# router.register('ticket', views.TicketViewSet)
# router.register('booking-item', views.BookingItemViewSet, basename='booking-item')

booking_router = routers.NestedDefaultRouter(router, 'booking', lookup='booking')
booking_router.register('items', views.BookingItemViewSet, basename='booking-items')

film_router = routers.NestedDefaultRouter(router, 'films', lookup='film')
film_router.register('images', views.FilmImageViewSet, basename='film-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(booking_router.urls)),
    path('', include(film_router.urls)),
    path('create-checkout-session', views.StripeCheckout.as_view()),
]

