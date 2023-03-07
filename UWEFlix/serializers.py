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