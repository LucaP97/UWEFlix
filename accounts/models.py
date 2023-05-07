from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class AccountManager(models.Manager):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Statement(models.Model):
    name = models.CharField(max_length=255)

class UweflixStatementItems(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, related_name='uweflix_statement_items')
    # uweflix orders
    order_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    order_object = GenericForeignKey('order_type', 'order_id')

class ClubStatementItems(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, related_name='club_statement_items')
    # club accounts
    account_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)
    account_id = models.PositiveIntegerField(null=True, blank=True)
    account_object = GenericForeignKey('account_type', 'account_id')

 
