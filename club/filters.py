from django_filters.rest_framework import FilterSet, IsoDateTimeFilter, DateTimeFromToRangeFilter, ChoiceFilter
from .models import *

class AccountFilter(FilterSet):
    order_placed_at = DateTimeFromToRangeFilter(field_name="order__placed_at")

    class Meta:
        model = Account
        fields = {
            'account_number': ['exact'],
        }


class DiscountRequestFilter(FilterSet):
    request_status = ChoiceFilter(choices=DiscountRequest.REQUEST_STATUS_CHOICES)

    class Meta:
        model = DiscountRequest
        fields = ['request_status']