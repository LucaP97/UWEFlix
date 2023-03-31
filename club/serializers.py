from django.apps import apps
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import *
import random
        
 
class ClubRepresentativeUserSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, default=get_random_string(length=12))

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def save(self, **kwargs):
        self.validated_data['username'] = str(random.randint(100000, 999999))
        return super().save(**kwargs)
    
            
class ClubRepresentativeSerializer(serializers.ModelSerializer): 
    user = ClubRepresentativeUserSerializer()

    class Meta:
        model = ClubRepresentative
        fields = ['id', 'date_of_birth', 'user', 'club']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username'] = str(random.randint(100000, 999999))
        generated_password = get_random_string(length=12)
        user_data['password'] = generated_password

        user_serializer = ClubRepresentativeUserSerializer(data=user_data)
        # user_serializer.is_valid(raise_exception=True)

        if not user_serializer.is_valid():
            print("user serializer errors: ", user_serializer.errors)
            raise serializers.ValidationError(user_serializer.errors)

        user = user_serializer.save()

        club_representative = ClubRepresentative.objects.create(user=user, **validated_data)
        club_representative.__dict__['generated_password'] = generated_password

        return club_representative
    

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user']['password'] = instance.__dict__.get('generated_password')
        return ret

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_number', 'street', 'city', 'post_code']

class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = ['landline_number', 'mobile_number', 'club_email']

# this needs to be redone, club serializer should be separate
class ClubSerializer(serializers.ModelSerializer):
    # this should be CreateClubSerializer
    address = AddressSerializer()
    contact_details = ContactDetailsSerializer()

    class Meta:
        model = Club
        fields = ['name', 'address', 'contact_details', 'club_number']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contact_details_data = validated_data.pop('contact_details')
        address = Address.objects.create(**address_data)
        contact_details = ContactDetails.objects.create(**contact_details_data)
        club = Club.objects.create(address=address, contact_details=contact_details, **validated_data)
        return club
    
######## accounts ########

class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymmentDetails
        fields = ['card_name', 'card_number', 'expiry_date']

class AccountSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailsSerializer()
    account_title = serializers.CharField(read_only=True)
    account_number = serializers.CharField(read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'club', 'account_number', 'account_title', 'account_title', 'discount_rate', 'payment_details']

    def create(self, validated_data):
        payment_details_data = validated_data.pop('payment_details')
        payment_details = PaymmentDetails.objects.create(**payment_details_data)

        validated_data['account_title'] = validated_data['club'].name
        validated_data['account_number'] = str(random.randint(100000, 999999))

        return Account.objects.create(payment_details=payment_details, **validated_data)
    
class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statements
        fields = ['amount_due']

    def create(self, validated_data):
        account_id = self.context['account_id']
        return Statements.objects.create(account_id=account_id, **validated_data)
        # return super().create(validated_data)