from django.conf import settings
from django.db import models
from django import forms
from django.core.validators import MinValueValidator
from django.contrib import admin
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
from uuid import uuid4
# from django.contrib.auth.password_validation import validate_password


## users
class CinemaManager(models.Model): # this will extend the User class
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()


# Uweflix items
class Film(models.Model):
    title = models.CharField(max_length=255, unique=True)
    age_rating = models.SmallIntegerField()
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    short_trailer_description = models.TextField(null=False)

    def __str__(self) -> str:
        return f'{self.title}'

class Screen(models.Model):
    screen_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()

    def __str__(self):
        return f'{self.screen_name}'

### need to remove 'null=true' from showing date -> db needs to be restarted for this 

class Showing(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.PROTECT, related_name='showing')
    film = models.ForeignKey(Film, on_delete=models.PROTECT, related_name='showing')
    showing_date = models.DateField(auto_now_add=False, null=True)
    showing_time = models.TimeField(auto_now_add=False)
    tickets_sold = models.SmallIntegerField(default=0)
    child_price = models.DecimalField(max_digits=5, decimal_places=2, default=3)
    student_price = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    adult_price = models.DecimalField(max_digits=5, decimal_places=2, default=7)

class Ticket(models.Model):
    TICKET_TYPE_STUDENT = 'S'
    TICKET_TYPE_ADULT = 'A'
    TICKET_TYPE_CHILD = 'C'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
        (TICKET_TYPE_ADULT, 'Adult'),
        (TICKET_TYPE_CHILD, 'Child'),
    ]

    ticket_type = models.CharField(max_length=1, choices=TICKET_TYPE_CHOICE, default=TICKET_TYPE_STUDENT)


### abstract objects

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items', null=True)
    ticket_type = models.CharField(max_length=255)
    quantity= models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, related_name='booking_item')

    class Meta:
        ## not sure if showing should be added to this list of unique constraints or not?
        unique_together = [['booking', 'ticket_type']]