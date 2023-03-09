from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Film)
admin.site.register(Screen)
admin.site.register(Ticket)
admin.site.register(Showing)