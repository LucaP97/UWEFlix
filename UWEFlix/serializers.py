from django.utils import dateformat
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

    showing_time = serializers.SerializerMethodField(method_name='showing_time_conversion')

    def showing_time_conversion(self, showing: Showing):
        return dateformat.format(showing.showing_time, 'jS F Y h:i:s A')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pk','film','screen','showing_time','ticket_amount']
        
        
        