from django.shortcuts import render
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Prefetch
from .serializers import *
from rest_framework import viewsets
from datetime import datetime, timedelta 
from dateutil.relativedelta import relativedelta
from .permissions import *
from datetime import timedelta

# from django.contrib.postgres.aggregates import ArrayAgg


# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_active=True)
    serializer_class = OrderSerializer
    

def current_month_club_orders():
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=1) + timedelta(days=32)
    last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

    return ClubOrder.objects.filter(
        Q(placed_at__gte=first_day_of_month) &
        Q(placed_at__lt=next_month) &
        Q(is_active=True)
    )

def current_month_credit():
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = now.replace(day=1) + timedelta(days=32)
    last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

    return Credit.objects.filter(
        Q(placed_at__gte=first_day_of_month) &
        Q(placed_at__lt=next_month)
    )

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
class UweflixStatementItemsViewSet(viewsets.ModelViewSet):
    # queryset = UweflixStatementItems.objects.all()
    serializer_class = UweflixStatementItemsSerializer

    def get_queryset(self):
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = now.replace(day=1) + timedelta(days=32)
        last_day_of_month = next_month.replace(day=1) - timedelta(days=1)

        orders = Order.objects.filter(placed_at__range=(first_day_of_month, last_day_of_month), is_active=True)

        return UweflixStatementItems.objects.filter(order_type=ContentType.objects.get_for_model(Order), order_id__in=orders)
    

### statements ###

class StatementViewSet(viewsets.ModelViewSet):
    queryset = (
        Statement.objects
        .prefetch_related(
            Prefetch("uweflix_statement_items__order_object__items__showing__price"),
            Prefetch("uweflix_statement_items__order_object__items__showing"),
            Prefetch("club_statement_items__account_object__club_order"),
        ).all()
    )
    serializer_class = StatementSerializer

    # permission_classes = [AccountManagerOnly]

