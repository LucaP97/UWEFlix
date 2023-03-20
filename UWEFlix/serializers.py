from django.utils import dateformat
from rest_framework import serializers
from .models import *

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'age_rating', 'duration', 'short_trailer_description', 'image_uri']


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen_name', 'capacity']

class SimpleScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen_name']


class ShowingSerializer(serializers.ModelSerializer):
    
    # film = FilmSerializer()
    class Meta:
        model = Showing
        fields = ['screen', 'film', 'showing_date', 'showing_time', 'child_price', 'student_price', 'adult_price']

    

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
            return booking_item.quantity * booking_item.showing.student_price
        elif booking_item.ticket_type == 'A':
            return booking_item.quantity * booking_item.showing.adult_price
        elif booking_item.ticket_type == 'C':
            return booking_item.quantity * booking_item.showing.child_price
        else:
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
    items = BookingItemSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, booking):
        return sum([BookingItemSerializer(item).get_total_price(item) for item in booking.items.all()])

    class Meta:
        model = Booking
        fields = ['id', 'items', 'total_price']
