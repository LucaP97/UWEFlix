from django.apps import apps
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from generic_relations.relations import GenericRelatedField
from .models import *
import random
        
# user serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class CreateAccountManagerSerializer(serializers.Serializer):
    user = UserCreateSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['first_name'] = user_data.pop('first_name')
        user_data['last_name'] = user_data.pop('last_name')

        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        return AccountManager.objects.create(user=user, **validated_data)


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
            raise serializers.ValidationError(user_serializer.errors)

        user = user_serializer.save()

        club_representative = ClubRepresentative.objects.create(user=user, **validated_data)
        club_representative.__dict__['generated_password'] = generated_password

        try:
            message = BaseEmailMessage(
                template_name='emails/club_representative_registration.html',
                context={'username': user_data['username'], 'password': user_data['password'], 'user': user_data}
            )
            message.send([user_data['email']])
        except BadHeaderError:
            pass

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
    

    


# class StatementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Statements
#         fields = ['amount_due']


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

class ClubBookingItemSerializer(serializers.ModelSerializer):
    
    TICKET_TYPE_STUDENT = 'S'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
    ]

    ticket_type = serializers.ChoiceField(choices=TICKET_TYPE_CHOICE, default=TICKET_TYPE_STUDENT, read_only=True)


    total_price = serializers.SerializerMethodField()

    

    showing_object = GenericRelatedField({
        Showing: ShowingSerializer(),
    })

    def get_total_price(self, booking_item:ClubBookingItem):
        return booking_item.quantity * booking_item.showing_object.price.student
    

    def validate_showing_object(self, club_booking_item:ClubBookingItem):
        if club_booking_item.showing_object.showing_date < timezone.now().date():
            raise serializers.ValidationError("Showing date must be in the future")
        return club_booking_item
    

    class Meta:
        model = ClubBookingItem
        # 'content_object',
        fields = ['id', 'club_booking', 'ticket_type', 'quantity', 'showing_object', 'total_price']


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
        club_booking_id = self.context['club_booking_id']
        showing_id = self.initial_data['showing_id']
        # ticket_type = self.initial_data['ticket_type']

        showing = Showing.objects.get(pk=showing_id)

        try:
            club_booking_item = ClubBookingItem.objects.get(club_booking_id=club_booking_id, showing_id=showing_id)#, ticket_type=ticket_type)
            current_quantity = club_booking_item.quantity
            total_quantity = current_quantity + value

            if value < 10:
                raise serializers.ValidationError("Quantity must be at least 10")
            if total_quantity > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        except ClubBookingItem.DoesNotExist:
            if value < 10:
                raise serializers.ValidationError("Quantity must be at least 10")
            if value > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')

        return value
    

    def save(self, **kwargs):
        club_booking_id = self.context['club_booking_id']
        showing_id = self.validated_data['showing_id']
        # ticket_type = self.validated_data['ticket_type']
        quantity = self.validated_data['quantity']

        try:
            club_booking_item = ClubBookingItem.objects.get(club_booking_id=club_booking_id, showing_id=showing_id)#, ticket_type=ticket_type)
            club_booking_item.quantity += quantity
            club_booking_item.save()
            self.instance = club_booking_item
        except ClubBookingItem.DoesNotExist:
            self.instance = ClubBookingItem.objects.create(club_booking_id=club_booking_id, showing_type=self.showing_content_type, **self.validated_data)

        return self.instance
    
    
    class Meta:
        model = ClubBookingItem
        fields = ['id', 'showing_id', 'ticket_type', 'quantity']


class UpdateClubBookingItemSerializer(serializers.ModelSerializer):

    def validate_quantity(self, value):
        club_booking_id = self.context['club_booking_id']
        showing_id = self.initial_data['showing_id']
        ticket_type = self.initial_data['ticket_type']

        showing = Showing.objects.get(pk=showing_id)

        try:
            club_booking_item = ClubBookingItem.objects.get(club_booking_id=club_booking_id, showing_id=showing_id, ticket_type=ticket_type)
            current_quantity = club_booking_item.quantity
            total_quantity = current_quantity + value

            if value < 10:
                raise serializers.ValidationError("Quantity must be at least 10")
            if total_quantity > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        except ClubBookingItem.DoesNotExist:
            if value < 10:
                raise serializers.ValidationError("Quantity must be at least 10")
            if value > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        return value


    class Meta:
        model = ClubBookingItem
        fields = ['quantity']


class ClubBookingSerialier(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    club_items = ClubBookingItemSerializer(many=True, required=False, read_only=True)
    total_price = serializers.SerializerMethodField()
    # discounted_price = serializers.SerializerMethodField()

    def validate_quantity(self, value):
        if value < 10:
            raise serializers.ValidationError("Quantity must be at least 10")
        return value

    def get_total_price(self, club_booking):
        return sum([ClubBookingItemSerializer(club_item).get_total_price(club_item) for club_item in club_booking.club_items.all()])
    
    # def get_discounted_price(self, booking):
    #     return self.get_total_price(booking) * (1 - booking.account.discount_rate)

    class Meta:
        model = ClubBooking
        fields = ['id', 'club_items', 'total_price']


### Club orders ###

class ClubOrderItemSerializer(serializers.ModelSerializer):
    showing_object = GenericRelatedField({
        Showing: ShowingSerializer(),
    })
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, club_order_item:ClubOrderItem):
        return club_order_item.quantity * club_order_item.showing_object.price.student
    
    class Meta:
        model = ClubOrderItem
        fields = ['id', 'club_order', 'showing_object', 'quantity', 'total_price']


class ClubOrderSerializer(serializers.ModelSerializer):
    club_items = ClubOrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    discounted_total_price = serializers.SerializerMethodField()

    def get_total_price(self, club_order):
        return sum([ClubOrderItemSerializer(item).get_total_price(item) for item in club_order.club_items.all()])
    
    def get_discounted_total_price(self, club_order):
        discount_amount = (self.get_total_price(club_order) * club_order.account.discount_rate) / 100
        return self.get_total_price(club_order) - discount_amount

    class Meta:
        model = ClubOrder
        fields = ['id', 'account', 'placed_at', 'payment_status', 'club_items', 'total_price', 'discounted_total_price']


class UpdateClubOrderSerializer(serializers.ModelSerializer):

    # was going to reduce the account balance here, but.
    # should it be done in accounts, when the club rep adds funds?
    # this would mean removing payment status for club also.

    class Meta:
        model = ClubOrder
        fields = ['payment_status']


class CreateClubOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        club_booking_id = serializers.UUIDField()

        def validate_club_booking_id(self, club_booking_id):
            if not ClubBooking.objects.filter(pk=club_booking_id).exists():
                raise serializers.ValidationError("No booking with the given ID was found.")
            if ClubBookingItem.objects.filter(club_booking_id=club_booking_id).count() == 0:
                raise serializers.ValidationError("The booking is empty.")
            return club_booking_id
        
        def validate(self, data):
            club_booking_id = data['club_booking_id']
            club_booking_items = ClubBookingItem.objects.select_related('showing_type').filter(club_booking_id=club_booking_id)

            for item in club_booking_items:
                showing = item.showing_object
                available_tickets = showing.screen.capacity - showing.tickets_sold
                if item.quantity > available_tickets:
                    raise serializers.ValidationError(f'There are {available_tickets} tickets remaining for the showing of {showing.film.title} on {showing.showing_date}.')
                showing.tickets_sold += item.quantity
                showing.save()

            return data
        
        def update_account_balance(self, club_order):
            total_price = sum([ClubOrderItemSerializer(item).get_total_price(item) for item in club_order.club_items.all()])
            discount_amount = (total_price * club_order.account.discount_rate) / 100
            discount_price = total_price - discount_amount
            club_order.account.account_balance += discount_price
            club_order.account.save()
        
        def save(self, **kwargs):
            club_booking_id = self.validated_data['club_booking_id']

            ## need to think here about getting the account from club
            account = Account.objects.get(id=self.context['account_id'])
            club_order = ClubOrder.objects.create(account=account)

            club_booking_items = ClubBookingItem.objects.select_related('showing_type').filter(club_booking_id=self.validated_data['club_booking_id'])
            club_order_items = [
                ClubOrderItem(
                    club_order=club_order,
                    showing_type=item.showing_type,
                    showing_id=item.showing_id,
                    ticket_type=item.ticket_type,
                    quantity=item.quantity
                ) for item in club_booking_items
            ]

            ClubOrderItem.objects.bulk_create(club_order_items)

            self.update_account_balance(club_order)

            ClubBooking.objects.filter(pk=club_booking_id).delete()

            # this is for signals, not sure if we need?
            # order_created.send_robust(sender=self.__class__, order=order)

            return club_order
        


######## accounts ########


class CreditSerializer(serializers.ModelSerializer):

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    class Meta:
        model = Credit
        fields = ['id', 'amount', 'placed_at']


# class CreditSerializer(serializers.ModelSerializer):
#     items = CreditItemSerializer(many=True)

#     class Meta:
#         model = Credit
#         fields = ['id', 'account', 'items']


class PaymentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymmentDetails
        fields = ['card_name', 'card_number', 'expiry_date']

class CreateAccountSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all())
    payment_details = PaymentDetailsSerializer()
    account_title = serializers.CharField(read_only=True)
    account_number = serializers.CharField(read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'club', 'account_number', 'account_title', 'discount_rate', 'payment_details']

    def create(self, validated_data):
        payment_details_data = validated_data.pop('payment_details')
        payment_details = PaymmentDetails.objects.create(**payment_details_data)

        validated_data['account_title'] = validated_data['club'].name
        validated_data['account_number'] = str(random.randint(100000, 999999))

        return Account.objects.create(payment_details=payment_details, **validated_data)


class AccountSerializer(serializers.ModelSerializer):
    club_order = ClubOrderSerializer(many=True, read_only=True)
    credit = CreditSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'club', 'account_title', 'discount_rate', 'club_order', 'credit', 'account_balance']



class AccountAddFundsSerializer(serializers.Serializer):
    credit = CreditSerializer()

    def update(self, instance, validated_data):
        credit_data = validated_data.pop('credit')
        amount = credit_data['amount']
        if amount > instance.account_balance:
            raise serializers.ValidationError("Amount must be less or equal to account balance.")
        instance.account_balance -= amount
        instance.save()

        credit = Credit.objects.create(account=instance, **credit_data)
        credit.save()
        
        credit_serializer = CreditSerializer(credit)
        return {'credit': credit_serializer.data}

    
    class Meta:
        model = Account
        fields = ['credit']


class DiscountRequestSerializer(serializers.ModelSerializer):
    club = serializers.CharField(source='account.club.name', read_only=True)
    placed_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    class Meta:
        model = DiscountRequest
        fields = ['id', 'club', 'account', 'amount', 'request_status', 'placed_at']

class CreateDiscountRequestSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context['user']

        if not hasattr(user, 'clubrepresentative'):
            raise serializers.ValidationError("You must be a club representative to request a discount.")
        elif not hasattr(user.clubrepresentative, 'club') or user.clubrepresentative.club.account is None:
            raise serializers.ValidationError("Your club must have an account to request a discount.")

        account = user.clubrepresentative.club.account
        discount_request = DiscountRequest.objects.create(account=account, **validated_data)
        return discount_request

    class Meta:
        model = DiscountRequest
        fields = ['id', 'account', 'amount']

class UpdateDiscountRequestSerializer(serializers.ModelSerializer):
    request_status = serializers.ChoiceField(choices=[(DiscountRequest.REQUEST_STATUS_APPROVED, 'Approve'),
                                                        (DiscountRequest.REQUEST_STATUS_REJECTED, 'Reject')])

    def update(self, instance, validated_data):
        status = validated_data['request_status']
        instance.request_status = status
        if status == 'A':
            instance.account.discount_rate = instance.amount
            instance.account.save()
        instance.save()
        
        return instance

    class Meta:
        model = DiscountRequest
        fields = ['request_status']