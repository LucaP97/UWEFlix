from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class UweflixAccounts(models.Model):
    order_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField()
    order_object = GenericForeignKey('order_type', 'order_id')

class ClubAccounts(models.Model):
    account_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    account_id = models.PositiveIntegerField()
    account_object = GenericForeignKey('account_type', 'account_id')