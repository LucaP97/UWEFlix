from django.utils import timezone
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import *
import datetime


### UWEFlix ###
Order = ContentType.objects.get(app_label='UWEFlix', model='order').model_class()
OrderItem = ContentType.objects.get(app_label='UWEFlix', model='orderitem').model_class()
Showing = ContentType.objects.get(app_label='UWEFlix', model='showing').model_class()

class ShowingSerializer(serializers.ModelSerializer):
    # ticket_price = serializers.SerializerMethodField()

    class Meta:
        model = Showing
        fields = ['id', 'screen', 'film', 'showing_date', 'showing_time']

    # def get_price_student(self, showing:Showing):
    #     if 
    #     return showing.price.student

class OrderItemSerializer(serializers.ModelSerializer):
    showing = ShowingSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['showing', 'ticket_type', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['student', 'placed_at', 'payment_status', 'items']



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
        fields = ['placed_at', 'club_items']

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['amount', 'placed_at']

class AccountSerializer(serializers.ModelSerializer):
    club_order = ClubOrderSerializer(many=True, read_only=True)
    credit = CreditSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['club', 'account_title', 'discount_rate', 'account_balance', 'club_order', 'credit']



### statements ###

class UweflixStatementItemsSerializer(serializers.ModelSerializer):
    order_object = GenericRelatedField({
        Order: OrderSerializer(),
    }, required=False)
    class Meta:
        model = UweflixStatementItems
        fields = ['statement', 'order_type', 'order_id', 'order_object']


class ClubStatementItemsSerializer(serializers.ModelSerializer):
    account_object = GenericRelatedField({
        Account: AccountSerializer(),
    }, required=False)
    class Meta:
        model = ClubStatementItems
        fields = ['statement', 'account_type', 'account_id', 'account_object']


class StatementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, read_only=True)
    uweflix_statement_items = UweflixStatementItemsSerializer(many=True, read_only=True)
    club_statement_items = ClubStatementItemsSerializer(many=True, read_only=True)

    def create(self, validated_data):
        now = timezone.now()
        statement = Statement.objects.create(name="statement: " + str(now.month) + "/" + str(now.year))

        # uweflix
        orders = Order.objects.filter(placed_at__month=now.month, placed_at__year=now.year)
        for order in orders:
            uweflix_statement_item = UweflixStatementItems.objects.create(
                statement=statement, order_object=order)
            uweflix_statement_item.save()

        # club
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
        fields = ['id', 'name', 'uweflix_statement_items', 'club_statement_items']





