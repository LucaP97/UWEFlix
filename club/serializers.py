from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import *
import random

def generate_random_number():
    while True:
        random_number = random.randint(100000, 999999)
        if not ClubRepresentative.objects.filter(club_representative_number=random_number).exists():
            return random_number

# def generate_password():
#     while True:
#         password = get_random_string(length=12)
#         if not ClubRepresentative.objects.filter(club_representative_number=random_number).exists():
#             return random_number
        
        
            
class ClubRepresentativeSerializer(serializers.ModelSerializer): 
    # user_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.CharField(max_length=255, write_only=True)

    username_string = generate_random_number()
    class Meta:
        model = ClubRepresentative
        fields = ['id', 'date_of_birth', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        username_string = generate_random_number()
        password_string = get_random_string(length=12)
        email = validated_data.pop('email')
        # first_name = validated_data.pop('first_name')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user_data = {
            'username': username_string,
            'email': email,
            'password': password_string,
            'first_name': first_name,
            'last_name': last_name
        }

        user_serializer = BaseUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        validated_data['user_id'] = user.id
        club_representative = ClubRepresentative.objects.create(user=user, **validated_data)

        return {'Club Representative Number': username_string, 'Password': password_string}

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_number', 'street', 'city', 'post_code']

class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = ['landline_number', 'mobile_number', 'club_email']

class ClubSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    contact_details = ContactDetailsSerializer()

    class Meta:
        model = Club
        fields = ['name', 'address', 'contact_details']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contact_details_data = validated_data.pop('contact_details')
        address = Address.objects.create(**address_data)
        contact_details = ContactDetails.objects.create(**contact_details_data)
        club = Club.objects.create(address=address, contact_details=contact_details, **validated_data)
        return club



        
