from django.conf import settings
from django.db import models
import random

# # Create your models here.
# class CinemaManager(models.Model): # this will extend the User class
#     pass

#### clubs ####
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
    club_number = models.SmallIntegerField()

    def __str__(self) -> str:
        return self.name

class ClubRepresentative(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    club = models.OneToOneField(Club, on_delete=models.PROTECT, related_name='club_representative')

    def __str__(self) -> str:
        return self.user.first_name
    
class PaymmentDetails(models.Model):
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()


#### accounts ####
class Account(models.Model):
    club = models.OneToOneField(Club, on_delete=models.PROTECT, related_name="account")
    # should be either surname and initial of employee (which employee?), or club name
    account_title = models.CharField(max_length=255)
    payment_details = models.OneToOneField(PaymmentDetails, on_delete=models.CASCADE)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    account_number = models.CharField(max_length=2)

    def __str__ (self) -> str:
        return self.account_title

class Statements(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='statement')
    amount_due = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class AccountManager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # date = models.DateField(auto_now_add=True)
