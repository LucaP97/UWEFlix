from django_filters.rest_framework import FilterSet, DateFilter
# from django_filters.widgets import DateRangeWidget
from .models import *

class ShowingFilter(FilterSet):
    showing_date = DateFilter()

    class Meta:
        model = Showing
        fields = ['showing_date']


