# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import *

# @receiver(post_save, sender=Order)
# def update_account_balance(sender, instance, created, **kwargs):
#     print("Signal called. Created:", created)
#     # if kwargs['created']:
#     if created:
#         instance.update_account_balance()