from django.contrib import admin

# Register your models here.
class CinemaManagerAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
