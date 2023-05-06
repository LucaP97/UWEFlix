from django.utils import dateformat, timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
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

class StudentUpdateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

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

        return CinemaManager.objects.create(user=user, **validated_data)

    class Meta():
        model = CinemaManager
        fields = ['id', 'user']

class TemporaryCinemaManagerRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.filter(employee__isnull=False))
    expiration_date = serializers.DateField(required=True)

    class Meta:
        model = CinemaManager
        fields = ['id', 'user', 'expiration_date']


class RegisterEmployeeSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['first_name'] = user_data.pop('first_name')
        user_data['last_name'] = user_data.pop('last_name')

        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        return Employee.objects.create(user=user, **validated_data)

    class Meta:
        model = Employee
        fields = ['id', 'user_id', 'user']


class FilmImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        film_id = self.context['film_id']
        return FilmImage.objects.create(film_id=film_id, **validated_data)
    
    class Meta:
        model = FilmImage
        fields = ['id', 'image']


class FilmSerializer(serializers.ModelSerializer):
    images = FilmImageSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'age_rating', 'duration', 'short_trailer_description', 'images']


class UpdateFilmSerializer(serializers.ModelSerializer):
    images = FilmImageSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'age_rating', 'duration', 'short_trailer_description', 'images', 'is_active']





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
        fields = ['id','student', 'adult', 'child']

class ShowingSerializer(serializers.ModelSerializer):
    price = PriceSerializer()
    film = serializers.PrimaryKeyRelatedField(queryset=Film.objects.filter(is_active=True))
    tickets_remaining = serializers.SerializerMethodField()
    
    def create(self, validated_data):
        price_data = validated_data.pop('price')
        price_serializer = PriceSerializer(data=price_data)
        price_serializer.is_valid(raise_exception=True)
        price = price_serializer.save()

        showing = Showing.objects.create(price=price, **validated_data)
        # Price.objects.create(showing=showing, **price_data)

        return showing
    
    def get_tickets_remaining(self, showing:Showing):
        return showing.screen.capacity - showing.tickets_sold

    class Meta:
        model = Showing
        fields = ['id', 'screen', 'film', 'showing_date', 'showing_time', 'price', 'tickets_remaining']


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
        
    
    def validate_showing(self, booking_item:BookingItem):
        if booking_item.showing.showing_date < timezone.today():
            raise serializers.ValidationError('The showing date must be in the future.')
        return booking_item
    
    
        
    
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_authenticated = self.context.get('request', None) and self.context['request'].user.is_authenticated

        if not user_authenticated:
            self.fields['ticket_type'].choices = [
                (ticket_type, label) for ticket_type, label in self.TICKET_TYPE_CHOICE if ticket_type != self.TICKET_TYPE_STUDENT
            ]

    def validate_showing_id(self, value):
        if not Showing.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No showing with the given ID was found.')
        if Showing.objects.get(pk=value).showing_date < timezone.now().date():
            raise serializers.ValidationError('The showing date must be in the future.')
        return value
    
    def validate_quantity(self, value):
        booking_id = self.context['booking_id']
        showing_id = self.initial_data['showing_id']
        ticket_type = self.initial_data['ticket_type']

        if not Showing.objects.filter(pk=showing_id).exists():
            raise serializers.ValidationError('No showing with the given ID was found.')

        showing = Showing.objects.get(pk=showing_id)

        try:
            booking_item = BookingItem.objects.get(booking_id=booking_id, showing_id=showing_id, ticket_type=ticket_type)
            current_quantity = booking_item.quantity
            total_quantity = current_quantity + value

            if total_quantity > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        except BookingItem.DoesNotExist:
            if value < 1:
                raise serializers.ValidationError('The quantity must be greater than 0.')
            if value > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
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
            self.instance = BookingItem.objects.create(booking_id=booking_id, **self.validated_data)
        
        return self.instance 


    class Meta:
        model = BookingItem
        fields = ['id', 'showing_id', 'ticket_type', 'quantity']

class UpdateBookingItemSerializer(serializers.ModelSerializer):

    def validate_quantity(self, value):
        booking_id = self.context['booking_id']
        showing_id = self.initial_data['showing_id']
        ticket_type = self.initial_data['ticket_type']

        showing = Showing.objects.get(pk=showing_id)

        try:
            booking_item = BookingItem.objects.get(booking_id=booking_id, showing_id=showing_id, ticket_type=ticket_type)
            current_quantity = booking_item.quantity
            total_quantity = current_quantity + value

            if total_quantity > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        except BookingItem.DoesNotExist:
            if value < 1:
                raise serializers.ValidationError('The quantity must be greater than 0.')
            if value > showing.screen.capacity - showing.tickets_sold:
                raise serializers.ValidationError(f'There are {showing.screen.capacity - showing.tickets_sold} tickets left for this showing.')
            
        return value

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
        

        def validate(self, data):
            booking_id = data['booking_id']
            booking_items = BookingItem.objects.select_related('showing__screen').filter(booking_id=booking_id)

            for item in booking_items:
                showing = item.showing
                available_seats = showing.screen.capacity - showing.tickets_sold
                if item.quantity > available_seats:
                    raise serializers.ValidationError(f'There are only {available_seats} seats remaining for the showing of {showing.film.title} on {showing.showing_date}.')
                showing.tickets_sold += item.quantity
                showing.save()

            return data


        def save(self, **kwargs):
            booking_id = self.validated_data['booking_id']

            print('context')
            print(self.context)
            if 'user' in self.context:
                student = Student.objects.get(user_id=self.context['user'].id)
            else:
                student = None

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