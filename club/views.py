from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import *
from .serializers import *
import random
from .tasks import *


### celery tasks

def say_hello(request):
    create_statements().delay()



class ClubRepresentativeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

# using this line for debugging purposes:
# class ClubRepresentativeViewSet(ModelViewSet):
    queryset = ClubRepresentative.objects.all()
    serializer_class = ClubRepresentativeSerializer

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        club_representative = ClubRepresentative.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ClubRepresentativeSerializer(club_representative)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ClubRepresentativeSerializer(club_representative, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    

class ClubViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


# class StatementsViewSet(ModelViewSet):
#     queryset = Statements.objects.all()
#     serializer_class = StatementSerializer

#     def get_serializer_context(self):
#         return {'account_id': self.kwargs['account_pk']}


### Booking ###

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.prefetch_related('items').all()
    serializer_class = BookingSerialier

class BookingItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddBookingItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateBookingItemSerializer
        return BookingItemSerializer
    
    def get_serializer_context(self):
        return {'booking_id': self.kwargs['booking_pk']}
    
    def get_queryset(self):
        # return BookingItem.objects.filter(booking__id=self.kwargs['booking_pk'])
        return BookingItem.objects.prefetch_related('showing_object', 'showing_object__price').filter(booking__id=self.kwargs['booking_pk'])





