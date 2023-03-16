from django.conf import settings
from django.db import models
from django import forms
from django.contrib import admin
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.password_validation import validate_password

# class Address(models.Model): 
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     postcode = models.CharField(max_length=255)

#     def __str__(self) -> str:
#         return self.street_number + ' ' + self.street


# class ContactDetails(models.Model):
#     mobile_number = models.CharField(max_length=50)
#     landline_number = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)

#     def __str__(self) -> str:
#         return self.email


# class Club(models.Model):
#     address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
#     contact_details = models.ForeignKey(ContactDetails, on_delete=models.CASCADE, null=True)
#     club_name = models.CharField(max_length=255)

#     def __str__(self) -> str:
#         return self.club_name


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

class Film(models.Model):
    title = models.CharField(max_length=255, unique=True)
    age_rating = models.SmallIntegerField()
    duration = models.DurationField(default=0)
    short_trailer_description = models.TextField(null=False)

    def __str__(self):
        return f'{self.title}'

class Screen(models.Model):
    screen_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()

    def __str__(self):
        return f'{self.screen_name}'

class Showing(models.Model):
    screen = models.OneToOneField(Screen, on_delete=models.PROTECT, related_name='screen')
    film = models.ForeignKey(Film, on_delete=models.PROTECT, related_name='showing')
    showing_time = models.DateTimeField(auto_now=False)
    tickets_sold = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self) -> str:
        return f'film:{self.film.title} .... screen:{self.screen}'

class Ticket(models.Model):
    TICKET_TYPE_STUDENT = 'S'
    TICKET_TYPE_ADULT = 'A'
    TICKET_TYPE_CHILD = 'C'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
        (TICKET_TYPE_ADULT, 'Adult'),
        (TICKET_TYPE_CHILD, 'Child'),
    ]

    PRICE_CHOICE = [
        (TICKET_TYPE_STUDENT, '10'),
        (TICKET_TYPE_ADULT, '15'),
        (TICKET_TYPE_CHILD, '5'),
    ]
    
    showing = models.ForeignKey(Showing, on_delete=models.PROTECT,blank=True,null=True)
    
    ticket_price = models.CharField(max_length=1, choices=PRICE_CHOICE, default=TICKET_TYPE_STUDENT)    
    ticket_type = models.CharField(max_length=1, choices=TICKET_TYPE_CHOICE, default=TICKET_TYPE_STUDENT)
    
    film = models.CharField(max_length=100,blank=True,null=True)
    screen = models.CharField(max_length=100,blank=True,null=True)
    showing_time = models.CharField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return f'type:{self.ticket_type} .... film:{self.film} .... showing_ref:{self.showing}'
    
class Booking(models.Model):
    showing_ref = models.CharField(max_length=100,blank=True,null=True)
    
    film = models.CharField(max_length=100,blank=True,null=True)
    screen = models.CharField(max_length=100,blank=True,null=True)
    showing_time = models.CharField(max_length=100,blank=True,null=True)
    
    tkt_student_amnt = models.PositiveIntegerField(name='student',default=0)
    tkt_adult_amnt = models.PositiveIntegerField(name='adult',default=0)
    tkt_child_amnt = models.PositiveIntegerField(name='child',default=0)
    
    total_price = models.DecimalField(max_digits=8, decimal_places=2,default=0.0, blank=True, null=True)

    def __str__(self) -> str:
        return f'showing_ref:{self.showing_ref} .... film:{self.film}'
    