from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import *
from .filters import *
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


# class AddAccountViewSet(ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = AddAccountSerializer

class AccountViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    queryset = Account.objects.all()
    # serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAccountSerializer
        elif self.request.method == 'PUT':
            return AccountAddFundsSerializer
        elif self.request.method == 'PATCH':
            return CreateAccountSerializer
        return AccountSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Account.objects.all()
        account_id = user.clubrepresentative.club.account.id
        return Account.objects.filter(id=account_id)



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




class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    # for now, associating the order with the user ID (which is linked to the club rep), rather than the account
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'account_id': self.request.user.clubrepresentative.club.account.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    # this should check if club rep is associated with 

    # only club reps from the associated club's account can see their own orders
    # club, club rep, account

    def get_queryset(self):
        user = self.request.user
        # account_id = user.clubrepresentative.club.account.id

        ### this should be enough for the implementation, needs testing

        if user.is_staff:
            return Order.objects.all()
        
        account_id = user.clubrepresentative.club.account.id
        return Order.objects.filter(account_id=account_id)
    

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CreditViewSet(ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer


# class CreditViewSet(ModelViewSet):
#     queryset = Credit.objects.all()
#     serializer_class = CreditSerializer
