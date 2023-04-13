from .models import *
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField


Order = ContentType.objects.get(app_label='UWEFlix', model='order').model_class()
Account = ContentType.objects.get(app_label='club', model='account').model_class()


class UweflixAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['student', 'placed_at', 'payment_status', 'items']


class ClubAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['club', 'placed_at', 'account', 'account_title', 'discount_rate', 'account_balance']