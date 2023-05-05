from django.contrib import admin
from . models import *

admin.site.register(Booking)
admin.site.register(BookingItem)
admin.site.register(Order)
admin.site.register(OrderItem)

