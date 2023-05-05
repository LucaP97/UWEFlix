from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
import random
from uuid import uuid4
from datetime import datetime

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
    account_number = models.CharField(max_length=2, unique=True)
    account_balance = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__ (self) -> str:
        return self.account_title
    


class Credit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    placed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)



class AccountManager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



### orders ###

class ClubOrder(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    # ticket_type = models.CharField(max_length=1, default='S')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='club_order')

    # handled by signals
    # def update_account_balance(self):
    #     try:
    #         total_price = sum([item.total_price() for item in self.items.all()])
    #         discount_amount = (total_price * self.account.discount_rate) / 100
    #         discount_price = total_price - discount_amount
    #         self.account.account_balance += discount_price
    #         self.account.save()
    #         print(f"Total Price: {total_price}, Discount Amount: {discount_amount}, Discount Price: {discount_price}, New Account Balance: {self.account.account_balance}")
    #     except Exception as e:
    #         print(f"Error updating account balance: {e}")



class ClubOrderItem(models.Model):
    club_order = models.ForeignKey(ClubOrder, on_delete=models.PROTECT, related_name='club_items')
    # content types for showing
    showing_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    showing_id = models.PositiveIntegerField(null=True, blank=True)
    showing_object = GenericForeignKey('showing_type', 'showing_id')
    
    ticket_type = models.CharField(max_length=1, default='S')
    quantity = models.PositiveSmallIntegerField()
    


### booking ###

# should this include the account? 
class ClubBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class ClubBookingItem(models.Model):
    club_booking = models.ForeignKey(ClubBooking, on_delete=models.CASCADE, related_name='club_items')
    ticket_type = models.CharField(max_length=1, default='S')
    quantity = models.PositiveSmallIntegerField()
    # content types for showing
    showing_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    showing_id = models.PositiveIntegerField(null=True, blank=True)
    showing_object = GenericForeignKey('showing_type', 'showing_id')

    # class Meta:
    #     unique_together = ('booking', 'showing_type', 'showing_id')
