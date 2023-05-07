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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cinema_manager')
    expiration_date = models.DateField(null=True, blank=True)

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


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')


class CardDetails(models.Model):
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    card_details = models.ForeignKey(CardDetails, on_delete=models.CASCADE, related_name='customer', null=True)


# Uweflix items
class Film(models.Model):
    title = models.CharField(max_length=255, unique=True)
    age_rating = models.SmallIntegerField()
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    short_trailer_description = models.TextField(null=False)
    is_active = models.BooleanField(default=True)
    

    def __str__(self) -> str:
        return f'{self.title}'
    

class FilmImage(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cinema/images')

class Screen(models.Model):
    screen_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()

    def __str__(self):
        return f'{self.screen_name}'

### need to remove 'null=true' from showing date -> db needs to be restarted for this 

class Price(models.Model):
    child = models.DecimalField(max_digits=5, decimal_places=2, default=3)
    student = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    adult = models.DecimalField(max_digits=5, decimal_places=2, default=7)


class Showing(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.PROTECT, related_name='showing')
    film = models.ForeignKey(Film, on_delete=models.PROTECT, related_name='showing')
    showing_date = models.DateField(auto_now_add=False, null=True)
    showing_time = models.TimeField(auto_now_add=False)
    tickets_sold = models.SmallIntegerField(default=0)
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='showing')

### abstract objects

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)
    cancellation_request = models.BooleanField(default=False)

    # class Meta:
    #     permissions = [
    #         ('cancel_order', 'Can cancel order')
    #     ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    showing = models.ForeignKey(Showing, on_delete=models.PROTECT, related_name='orderitems')
    ticket_type = models.CharField(max_length=255)
    quantity = models.PositiveSmallIntegerField()


class OrderCancellationRequest(models.Model):
    CANCELLATION_STATUS_PENDING = 'P'
    CANCELLATION_STATUS_APPROVED = 'A'
    CANCELLATION_STATUS_REJECTED = 'R'
    CANCELLATION_STATUS_CHOICES = [
        (CANCELLATION_STATUS_PENDING, 'Pending'),
        (CANCELLATION_STATUS_APPROVED, 'Approved'),
        (CANCELLATION_STATUS_REJECTED, 'Rejected')
    ]

    cancellation_status = models.CharField(max_length=1, choices=CANCELLATION_STATUS_CHOICES, default=CANCELLATION_STATUS_PENDING)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='cancellation')
    placed_at = models.DateField(auto_now_add=True)


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