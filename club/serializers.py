from django.apps import apps
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from generic_relations.relations import GenericRelatedField
from .models import *
import random
        
# user serializer
class ClubRepresentativeUserSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, default=get_random_string(length=12))

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def save(self, **kwargs):
        self.validated_data['username'] = str(random.randint(100000, 999999))
        return super().save(**kwargs)
    
# profile serializer
class ClubRepresentativeSerializer(serializers.ModelSerializer): 
    user = ClubRepresentativeUserSerializer()

    class Meta:
        model = ClubRepresentative
        fields = ['id', 'user_id', 'date_of_birth', 'user', 'club']

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
    


# class StatementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Statements
#         fields = ['amount_due']

#     def create(self, validated_data):
#         account_id = self.context['account_id']
#         return Statements.objects.create(account_id=account_id, **validated_data)
#         # return super().create(validated_data)


### Content Types ###

Showing = ContentType.objects.get(app_label='UWEFlix', model='showing').model_class()

class ShowingSerializer(serializers.ModelSerializer):
    price_student = serializers.SerializerMethodField()

    class Meta:
        model = Showing
        fields = ['id', 'screen', 'film', 'showing_date', 'showing_time', 'price_student']

    def get_price_student(self, showing:Showing):
        return showing.price.student 



#### booking ####

class BookingItemSerializer(serializers.ModelSerializer):
    
    TICKET_TYPE_STUDENT = 'S'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
    ]

    ticket_type = serializers.ChoiceField(choices=TICKET_TYPE_CHOICE, default=TICKET_TYPE_STUDENT, read_only=True)


    total_price = serializers.SerializerMethodField()

    

    showing_object = GenericRelatedField({
        Showing: ShowingSerializer(),
    })

    def get_total_price(self, booking_item:BookingItem):
        return booking_item.quantity * booking_item.showing_object.price.student
    

    class Meta:
        model = BookingItem
        # 'content_object',
        fields = ['id', 'booking', 'ticket_type', 'quantity', 'showing_object', 'total_price']


class AddBookingItemSerializer(serializers.ModelSerializer):
    TICKET_TYPE_STUDENT = 'S'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
    ]

    ticket_type = serializers.ChoiceField(choices=TICKET_TYPE_CHOICE, default=TICKET_TYPE_STUDENT, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.showing_content_type = ContentType.objects.get(app_label='UWEFlix', model='showing')

    def validate_showing_id(self, value):
        if not Showing.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No showing with the given ID was found.")
        return value
    
    def validate_quantity(self, value):
        if value < 10:
            raise serializers.ValidationError("Quantity must be at least 10")
        return value
    
    def save(self, **kwargs):
        booking_id = self.context['booking_id']
        showing_id = self.validated_data['showing_id']
        # ticket_type = self.validated_data['ticket_type']
        quantity = self.validated_data['quantity']

        try:
            booking_item = BookingItem.objects.get(booking_id=booking_id, showing_id=showing_id)#, ticket_type=ticket_type)
            booking_item.quantity += quantity
            booking_item.save()
            self.instance = booking_item
        except BookingItem.DoesNotExist:
            self.instance = BookingItem.objects.create(booking_id=booking_id, showing_type=self.showing_content_type, **self.validated_data)

        return self.instance
    
    
    class Meta:
        model = BookingItem
        fields = ['id', 'showing_id', 'ticket_type', 'quantity']


class UpdateBookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ['quantity']


class BookingSerialier(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = BookingItemSerializer(many=True, required=False, read_only=True)
    total_price = serializers.SerializerMethodField()

    def validate_quantity(self, value):
        if value < 10:
            raise serializers.ValidationError("Quantity must be at least 10")
        return value

    def get_total_price(self, booking):
        return sum([BookingItemSerializer(item).get_total_price(item) for item in booking.items.all()])

    class Meta:
        model = Booking
        fields = ['id', 'items', 'total_price']