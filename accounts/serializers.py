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
# club repuires:
# - order
#   - orderitem
#   - showing
# - credit
# - account


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


# class StatementSerializer(serializers.ModelSerializer):
#     order_object = GenericRelatedField({
#         Order: OrderSerializer(),
#     })
#     account_object = GenericRelatedField({
#         Account: AccountSerializer(),
#     })

#     class Meta:
#         model = Statement
#         fields = ['order_object', 'account_object']


# class CreateStatementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Statement
#         fields = ['name', 'order_type', 'order_id', 'account_type', 'account_id']

#     # def create(self, validated_data):
