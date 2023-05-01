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
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, SAFE_METHODS
from .models import *
from .filters import *
from .serializers import *
import random
from .tasks import *
from .permissions import *


## account manager

class AccountManagerViewSet(ModelViewSet):
    queryset = AccountManager.objects.all()
    serializer_class = CreateAccountManagerSerializer

    permission_classes = [IsCinemaManagerOrStaff]



# class ClubRepresentativeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
class ClubRepresentativeViewSet(ModelViewSet):
    queryset = ClubRepresentative.objects.all()
    serializer_class = ClubRepresentativeSerializer

    # def create(self, request, *args, **kwargs):

    #     return super().create(request, *args, **kwargs)
    
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
        
    permission_classes = [IsCinemaManagerOrStaff]

    

class ClubViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    permission_classes = [IsCinemaManagerOrAccountManagerReadOnly]


# class AddAccountViewSet(ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = AddAccountSerializer

class AccountViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    queryset = Account.objects.all()
    # serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAccountSerializer
        elif self.request.method == 'PUT':
            return AccountAddFundsSerializer
        elif self.request.method == 'PATCH':
            return CreateAccountSerializer
        return AccountSerializer

    def get_queryset(self):

        if hasattr(self.request.user, 'accountmanager'):
            return Account.objects.all()
        account_id = self.request.user.clubrepresentative.club.account.id
        return Account.objects.filter(id=account_id)
        
    permission_classes = [IsAccountManagerOrClubRepresentativeOnly]
        
    # permission_classes = [IsClubRepresentativeOrAccountManager]
        
    


### Booking ###

class ClubBookingViewSet(ModelViewSet):
    queryset = ClubBooking.objects.prefetch_related('club_items').all()
    serializer_class = ClubBookingSerialier

class ClubBookingItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddBookingItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateClubBookingItemSerializer
        return ClubBookingItemSerializer
    
    def get_serializer_context(self):
        return {'club_booking_id': self.kwargs['club_booking_pk']}
    
    def get_queryset(self):
        # return BookingItem.objects.filter(booking__id=self.kwargs['booking_pk'])
        print(self.kwargs)
        return ClubBookingItem.objects.prefetch_related('showing_object', 'showing_object__price').filter(club_booking__id=self.kwargs['club_booking_pk'])




class ClubOrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    # for now, associating the order with the user ID (which is linked to the club rep), rather than the account
    def create(self, request, *args, **kwargs):
        serializer = CreateClubOrderSerializer(data=request.data, context={'account_id': self.request.user.clubrepresentative.club.account.id})
        serializer.is_valid(raise_exception=True)
        club_order = serializer.save()
        serializer = ClubOrderSerializer(club_order)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateClubOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateClubOrderSerializer
        return ClubOrderSerializer
    
    # this should check if club rep is associated with 

    # only club reps from the associated club's account can see their own orders
    # club, club rep, account

    def get_queryset(self):
        user = self.request.user
        # account_id = user.clubrepresentative.club.account.id

        ### this should be enough for the implementation, needs testing

        if user.is_staff:
            return ClubOrder.objects.all()
        
        account_id = user.clubrepresentative.club.account.id
        return ClubOrder.objects.filter(account_id=account_id)
    

class ClubOrderItemViewSet(ModelViewSet):
    queryset = ClubOrderItem.objects.all()
    serializer_class = ClubOrderItemSerializer


class CreditViewSet(ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

    permission_classes = [IsAccountManagerOrClubRepresentativeOnly]


# class CreditViewSet(ModelViewSet):
#     queryset = Credit.objects.all()
#     serializer_class = CreditSerializer
