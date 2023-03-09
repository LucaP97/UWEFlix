from django.conf import settings
from django.db import models

# # Create your models here.
# class CinemaManager(models.Model): # this will extend the User class
#     pass

class ClubRepresentative(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Address(models.Model):
    street_number = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.street_number + ' ' + self.street


class ContactDetails(models.Model):
    mobile_number = models.CharField(max_length=50)
    landline_number = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email

class Club(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.CASCADE, null=True)
    club_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.club_name
    
class PaymentDetails(models.Model):
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()

class Account(models.Model):
    club = models.OneToOneField(Club, on_delete=models.PROTECT)
    payment_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)
    account_title = models.CharField(max_length=255, primary_key=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
