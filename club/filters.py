from django_filters.rest_framework import FilterSet, IsoDateTimeFilter, DateTimeFromToRangeFilter
from .models import *

class AccountFilter(FilterSet):
    order_placed_at = DateTimeFromToRangeFilter(field_name="order__placed_at")

    class Meta:
        model = Account
        fields = {
            'account_number': ['exact'],
        }
