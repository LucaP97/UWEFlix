from django_filters.rest_framework import FilterSet, DateFilter
from django_filters.widgets import DateRangeWidget
from .models import *

# class FilmFilter(FilterSet):
#     class Meta:
#         model = Film
#         fields = {
#             # needs to be changed eventually, filtering for movies shouldnt be exact
#             'title': ['exact']
#         }

# date filter is technically working, but is not user friendly.
class ShowingFilter(FilterSet):
    showing_date = DateFilter()

    class Meta:
        model = Showing
        fields = ['showing_date']