from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    pass

class Film(models.Model):
    title = models.CharField(max_length=255, unique=True)
    age_rating = models.SmallIntegerField()
    duration = models.DurationField()
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
    tickets_sold = models.SmallIntegerField(default=0)

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

    showing = models.OneToOneField(Showing, on_delete=models.PROTECT)

    PRICE_CHOICE = [
        (TICKET_TYPE_STUDENT, '10'),
        (TICKET_TYPE_ADULT, '15'),
        (TICKET_TYPE_CHILD, '5'),
    ]

    ticket_price = models.CharField(max_length=1, choices=PRICE_CHOICE)

class Customer(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self) -> str:
        return self.customer.username
    
class Booking(models.Model):
    booking_ref = models.CharField(max_length=6,blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True, related_name= 'booking')
    film = models.ForeignKey(Film,on_delete=models.SET_NULL,null=True, related_name= 'booking')
    screen = models.CharField(max_length=100,blank=True,null=True)
    showing_time = models.DateTimeField(auto_now=False,blank=True,null=True)
    ticket_quantity = models.IntegerField(default=0)

    
    
    
    
    