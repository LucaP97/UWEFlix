from django.utils import timezone
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import *
import datetime
from django.db.models import Q
from datetime import timedelta


### UWEFlix ###
Order = ContentType.objects.get(app_label='UWEFlix', model='order').model_class()
OrderItem = ContentType.objects.get(app_label='UWEFlix', model='orderitem').model_class()
Showing = ContentType.objects.get(app_label='UWEFlix', model='showing').model_class()

class ShowingSerializer(serializers.ModelSerializer):
    ticket_price = serializers.SerializerMethodField()

    class Meta:
        model = Showing
        fields = ['id']

class OrderItemSerializer(serializers.ModelSerializer):
    showing = ShowingSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order_item:OrderItem):
        if order_item.ticket_type == 'S':
            return order_item.quantity * order_item.showing.price.student
        elif order_item.ticket_type == 'A':
            return order_item.quantity * order_item.showing.price.adult
        elif order_item.ticket_type == 'C':
            return order_item.quantity * order_item.showing.price.child
        else:
            return 0

    class Meta:
        model = OrderItem
        fields = ['showing', 'ticket_type', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order:Order):
        return sum([OrderItemSerializer(item).get_total_price(item) for item in order.items.all()])

    class Meta:
        model = Order
        fields = ['student', 'placed_at', 'payment_status', 'items', 'total_price']



### club ###


Account = ContentType.objects.get(app_label='club', model='account').model_class()
ClubOrder = ContentType.objects.get(app_label='club', model='cluborder').model_class()
ClubOrderItem = ContentType.objects.get(app_label='club', model='cluborderitem').model_class()
Credit = ContentType.objects.get(app_label='club', model='credit').model_class()

class ClubOrderItemSerializer(serializers.ModelSerializer):
    showing_object = GenericRelatedField({
        Showing: ShowingSerializer(),
    })

    class Meta:
        model = ClubOrderItem
        fields = ['showing_object', 'ticket_type', 'quantity']

class ClubOrderSerializer(serializers.ModelSerializer):
    club_items = ClubOrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = ClubOrder
        fields = ['id', 'placed_at', 'club_items', 'total_paid']

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['amount', 'placed_at']

class AccountSerializer(serializers.ModelSerializer):
    club_order = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['club', 'account_title', 'discount_rate', 'account_balance', 'club_order', 'credit']

    def get_club_order(self, obj):
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = now.replace(day=1) + timedelta(days=32)

        club_orders = obj.club_order.filter(
            Q(placed_at__gte=first_day_of_month) &
            Q(placed_at__lt=next_month) &
            Q(is_active=True)
        )
        return ClubOrderSerializer(club_orders, many=True).data

    def get_credit(self, obj):
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = now.replace(day=1) + timedelta(days=32)

        credits = obj.credit.filter(
            Q(placed_at__gte=first_day_of_month) &
            Q(placed_at__lt=next_month)
        )
        return CreditSerializer(credits, many=True).data




### statements ###

class UweflixStatementItemsSerializer(serializers.ModelSerializer):
    order_object = GenericRelatedField({
        Order: OrderSerializer(),
    }, required=False)

    # uweflix_total = serializers.CharField()

    class Meta:
        model = UweflixStatementItems
        fields = ['order_id', 'order_object']


class ClubStatementItemsSerializer(serializers.ModelSerializer):
    account_object = GenericRelatedField({
        Account: AccountSerializer(),
    }, required=False)
    class Meta:
        model = ClubStatementItems
        fields = ['account_type', 'account_id', 'account_object']


class StatementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, read_only=True)
    uweflix_statement_items = UweflixStatementItemsSerializer(many=True, read_only=True)
    club_statement_items = ClubStatementItemsSerializer(many=True, read_only=True)
    uweflix_total = serializers.SerializerMethodField()
    club_total = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_uweflix_total(self, statement):
        return sum([OrderSerializer(item.order_object).data['total_price'] for item in statement.uweflix_statement_items.all()])
    
    def get_club_total(self, statement):
        return sum([sum(order.total_paid for order in item.account_object.club_order.all()) for item in statement.club_statement_items.all()])
    
    def get_total(self, statement):
        return sum([OrderSerializer(item.order_object).data['total_price'] for item in statement.uweflix_statement_items.all()]) + sum([sum(order.total_paid for order in item.account_object.club_order.all()) for item in statement.club_statement_items.all()])



    def create(self, validated_data):
        now = timezone.now()
        statement_name = "statement: " + str(now.month) + "/" + str(now.year)

        # Delete existing statements with the same name
        Statement.objects.filter(name=statement_name).delete()

        statement = Statement.objects.create(name=statement_name)

        # uweflix
        orders = Order.objects.filter(placed_at__month=now.month, placed_at__year=now.year)
        for order in orders:
            uweflix_statement_item = UweflixStatementItems.objects.create(
                statement=statement, order_object=order)
            uweflix_statement_item.save()

        ## club
        accounts = Account.objects.all()
        for account in accounts:
            club_orders = ClubOrder.objects.filter(account=account, placed_at__month=now.month, placed_at__year=now.year)
            credits = Credit.objects.filter(account=account, placed_at__month=now.month, placed_at__year=now.year)

            if club_orders.exists() or credits.exists():
                club_statement_item = ClubStatementItems.objects.create(
                    statement=statement, account_object=account)
                club_statement_item.save()

        return statement


    class Meta:
        model = Statement
        fields = ['id', 'name', 'uweflix_statement_items', 'club_statement_items', 'uweflix_total', 'club_total', 'total']
