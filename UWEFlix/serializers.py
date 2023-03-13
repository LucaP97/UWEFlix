from rest_framework import serializers
from .models import *

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['title', 'age_rating', 'duration', 'short_trailer_description']


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen_name', 'capacity']


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ['screen', 'film', 'showing_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['showing_time'] = instance.showing_time.strftime('%Y-%m-%d %H:%M:%S')
        return representation
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_ref','customer','film','screen','showing_time','ticket_quantity']
        extra_kwargs = {
            'film':{'read_only':True},
            'screen':{'read_only':True},
            'showing_time':{'read_only':True}
        }
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['film','showing_time', 'screen','customer']
    