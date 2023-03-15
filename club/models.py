from django.conf import settings
from django.db import models
import random

# # Create your models here.
# class CinemaManager(models.Model): # this will extend the User class
#     pass

class Address(models.Model):
    street_number = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.street_number + ' ' + self.street

class ContactDetails(models.Model):
    landline_number = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    club_email = models.CharField(max_length=255, unique=True)

class Club(models.Model):
    name = models.CharField(max_length=255)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, related_name='club')
    contact_details = models.OneToOneField(ContactDetails, on_delete=models.PROTECT, related_name='club')

class ClubRepresentative(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    club_representative_number = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=255, null=True)
    # club = models.OneToOneField(Club, on_delete=models.PROTECT, related_name='club_representative')

    def __str__(self) -> str:
        return self.name
    
class PaymentDetails(models.Model):
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()

class Account(models.Model):
    club = models.OneToOneField(Club, on_delete=models.PROTECT)
    payment_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)
    account_title = models.CharField(max_length=255, primary_key=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
