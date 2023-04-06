from django.shortcuts import render
from django.utils.crypto import get_random_string
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import *
from .serializers import *
import random
from .tasks import *


### celery tasks

def say_hello(request):
    create_statements().delay()



class ClubRepresentativeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

# using this line for debugging purposes:
# class ClubRepresentativeViewSet(ModelViewSet):
    queryset = ClubRepresentative.objects.all()
    serializer_class = ClubRepresentativeSerializer

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)
    
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

    

class ClubViewSet(ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


# class StatementsViewSet(ModelViewSet):
#     queryset = Statements.objects.all()
#     serializer_class = StatementSerializer

#     def get_serializer_context(self):
#         return {'account_id': self.kwargs['account_pk']}

class BookingItemViewSet(ModelViewSet):
    queryset = BookingItem.objects.all()
    serializer_class = BookingItemSerializer


    


