from django.utils.crypto import get_random_string
import random
from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, SetPasswordSerializer
from .models import *


def generate_random_password():
    while True:
        random_password = get_random_string(length=12)
        if not ClubRepresentative.objects.filter(password=random_password).exists():
            return random_password
                
class ClubRepresentativeSerializer(serializers.ModelSerializer): 
    user_id = serializers.IntegerField()
    class Meta:
        model = ClubRepresentative
        fields = ['id', 'user_id', 'club_representative_number']

        # def generate_random_number(self):
        #     while True:
        #         random_number = random.randint(100000, 999999)
        #         if not ClubRepresentative.objects.filter(club_representative_number=random_number).exists():
        #             return random_number
    
       

        # def create(self, validated_data):
        #     # ClubRepresentative.password = generate_random_password()
        #     return super().create(validated_data)

        
