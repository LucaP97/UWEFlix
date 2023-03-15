from django.shortcuts import render
from django.utils.crypto import get_random_string
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import random

# Create your views here.
class ClubRepresentativeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = ClubRepresentative.objects.all()
    serializer_class = ClubRepresentativeSerializer

    


