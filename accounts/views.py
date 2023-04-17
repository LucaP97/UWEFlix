from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q, Prefetch
from .serializers import *
from rest_framework import viewsets
from datetime import datetime, timedelta 
from dateutil.relativedelta import relativedelta

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = now.replace(day=1) + timedelta(days=32)
        last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

        return Order.objects.filter(placed_at__range=(first_day_of_month, last_day_of_month))
    

def current_month_club_orders():
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=1) + timedelta(days=32)
    last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

    return ClubOrder.objects.filter(placed_at__range=(first_day_of_month, last_day_of_month))

def current_month_credit():
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=1) + timedelta(days=32)
    last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

    return Credit.objects.filter(placed_at__range=(first_day_of_month, last_day_of_month))

class AccountViewSet(viewsets.ModelViewSet):
    # queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        club_orders = current_month_club_orders()
        credits = current_month_credit()

        return Account.objects.prefetch_related(
            Prefetch('club_order', queryset=club_orders),
            Prefetch('credit', queryset=credits)
        )
