from django.utils import dateformat
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .signals import order_created
from .models import *


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class StudentRegistrationSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['first_name'] = user_data.pop('first_name')
        user_data['last_name'] = user_data.pop('last_name')
        
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        return Student.objects.create(user=user, **validated_data)

    class Meta: 
        model = Student
        fields = ['id', 'user', 'birth_date']


class CinemaManagerRegistrationSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['first_name'] = user_data.pop('first_name')
        user_data['last_name'] = user_data.pop('last_name')

        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        group = Group.objects.get(name='Cinema Manager')
        group.user_set.add(user)

        return CinemaManager.objects.create(user=user, **validated_data)

    class Meta():
        model = CinemaManager
        fields = ['id', 'user']


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'age_rating', 'duration', 'short_trailer_description', 'image_uri']


class SimpleFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['title']


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen_name', 'capacity']

class SimpleScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen_name']


class PriceSerializer(serializers.ModelSerializer):
    student = serializers.IntegerField()
    adult = serializers.IntegerField()
    child = serializers.IntegerField()
    class Meta:
        model = Price
        fields = ['student', 'adult', 'child']

class ShowingSerializer(serializers.ModelSerializer):
    price = PriceSerializer()
    
    def create(self, validated_data):
        price_data = validated_data.pop('price')
        price_serializer = PriceSerializer(data=price_data)
        price_serializer.is_valid(raise_exception=True)
        price = price_serializer.save()

        showing = Showing.objects.create(price=price, **validated_data)
        # Price.objects.create(showing=showing, **price_data)

        return showing

    class Meta:
        model = Showing
        fields = ['id', 'screen', 'film', 'showing_date', 'showing_time', 'price']

    


    

# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['ticket_type']

   
#### booking ####

class BookingItemSerializer(serializers.ModelSerializer):
    # need to create a simple serializer, that only shows the price of the ticket selected
    showing = ShowingSerializer()

    TICKET_TYPE_STUDENT = 'S'
    TICKET_TYPE_ADULT = 'A'
    TICKET_TYPE_CHILD = 'C'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
        (TICKET_TYPE_ADULT, 'Adult'),
        (TICKET_TYPE_CHILD, 'Child'),
    ]

    ticket_type = serializers.ChoiceField(choices=TICKET_TYPE_CHOICE)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, booking_item:BookingItem):
        if booking_item.ticket_type == 'S':
            return booking_item.quantity * booking_item.showing.price.student
        elif booking_item.ticket_type == 'A':
            return booking_item.quantity * booking_item.showing.price.adult
        elif booking_item.ticket_type == 'C':
            return booking_item.quantity * booking_item.showing.price.child
        else:
            # this should return raise exception
            return None
    
    class Meta:
        model = BookingItem
        fields = ['showing', 'ticket_type', 'quantity', 'total_price']

class AddBookingItemSerializer(serializers.ModelSerializer):
    TICKET_TYPE_STUDENT = 'S'
    TICKET_TYPE_ADULT = 'A'
    TICKET_TYPE_CHILD = 'C'

    TICKET_TYPE_CHOICE = [
        (TICKET_TYPE_STUDENT, 'Student'),
        (TICKET_TYPE_ADULT, 'Adult'),
        (TICKET_TYPE_CHILD, 'Child'),
    ]

    ticket_type = serializers.ChoiceField(choices=TICKET_TYPE_CHOICE)
    showing_id = serializers.IntegerField()

    def validate_showing_id(self, value):
        if not Showing.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No showing with the given ID was found.')
        return value

    def save(self, **kwargs):
        booking_id = self.context['booking_id']
        showing_id = self.validated_data['showing_id']
        ticket_type = self.validated_data['ticket_type']
        quantity = self.validated_data['quantity']

        try:
            booking_item = BookingItem.objects.get(booking_id=booking_id, showing_id=showing_id, ticket_type=ticket_type)
            booking_item.quantity += quantity
            booking_item.save()
            self.instance = booking_item
        except BookingItem.DoesNotExist:
            # here must create a new item
            self.instance = BookingItem.objects.create(booking_id=booking_id, **self.validated_data)
        
        return self.instance 


    class Meta:
        model = BookingItem
        fields = ['id', 'showing_id', 'ticket_type', 'quantity']

class UpdateBookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ['quantity']

class BookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = BookingItemSerializer(many=True, required=False, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, booking):
        return sum([BookingItemSerializer(item).get_total_price(item) for item in booking.items.all()])

    class Meta:
        model = Booking
        fields = ['id', 'items', 'total_price']


### orders

class OrderItemSerializer(serializers.ModelSerializer):
    showing = ShowingSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, booking_item:BookingItem):
        if booking_item.ticket_type == 'S':
            return booking_item.quantity * booking_item.showing.price.student
        elif booking_item.ticket_type == 'A':
            return booking_item.quantity * booking_item.showing.price.adult
        elif booking_item.ticket_type == 'C':
            return booking_item.quantity * booking_item.showing.price.child
        else:
            # this should return raise exception
            return None
    class Meta:
        model = OrderItem
        fields = ['id', 'showing', 'ticket_type', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order):
        return sum([OrderItemSerializer(item).get_total_price(item) for item in order.items.all()])
    
    class Meta:
        model = Order
        fields = ['id', 'student', 'placed_at', 'payment_status', 'items', 'total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    with transaction.atomic():
        booking_id = serializers.UUIDField()

        def validate_booking_id(self, booking_id):
            if not Booking.objects.filter(pk=booking_id).exists():
                raise serializers.ValidationError('No booking with the given ID was found.')
            if BookingItem.objects.filter(booking_id=booking_id).count() == 0:
                raise serializers.ValidationError('The booking is empty.')
            return booking_id

        def save(self, **kwargs):
            booking_id = self.validated_data['booking_id']

            (student, created) = Student.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(student=student)

            # this is currently a queryset, we want to turn it into a collection via a list comprehension
            booking_items = BookingItem.objects.select_related('showing').filter(booking_id=self.validated_data['booking_id'])
            order_items = [
                OrderItem(
                    order=order,
                    showing=item.showing,
                    ticket_type=item.ticket_type,
                    # price is required here
                    quantity=item.quantity
                ) for item in booking_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Booking.objects.filter(pk=booking_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order