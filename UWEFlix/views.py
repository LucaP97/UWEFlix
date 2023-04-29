from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import *
from .permissions import *


# student
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (student, created) = Student.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentRegistrationSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentRegistrationSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

class CinemaManagerViewSet(ModelViewSet):
    queryset = CinemaManager.objects.all()
    serializer_class = CinemaManagerRegistrationSerializer


# films
class FilmViewSet(ModelViewSet):
    queryset = Film.objects.prefetch_related('images').all()
    serializer_class = FilmSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = FilmFilter
    search_fields = ['title', 'short_trailer_description']

    def destroy(self, request, *args, **kwargs):
        if Showing.objects.filter(film_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Film cannot be deleted because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    permission_classes = [IsCinemaManagerOrReadOnly]
    
class FilmImageViewSet(ModelViewSet):
    serializer_class = FilmImageSerializer

    def get_serializer_context(self):
        return {'film_id': self.kwargs['film_pk']}
    
    def get_queryset(self):
        return FilmImage.objects.filter(film_id=self.kwargs['film_pk'])
    
    permission_classes = [IsCinemaManagerOrReadOnly]

# screens
class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

    filter_backends = [SearchFilter]
    search_fields = ['screen_name']

    permission_classes = [IsCinemaManagerOrReadOnly]

# showings
# only issue is showing_time doesnt appear in the default form
class ShowingViewSet(ModelViewSet):
    queryset = Showing.objects.select_related('film', 'screen').all()
    serializer_class = ShowingSerializer

    #### the 'get_serializer_class' is wrong, need to think how to implement <<<<<<
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return SimpleFilmSerializer
    #     else:
    #         return FilmSerializer
        

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ShowingFilter
    search_fields = ['film__title']
    permission_classes = [IsCinemaManagerOrReadOnly]

# class TicketViewSet(ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer


#### booking ####
 
class BookingViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Booking.objects.prefetch_related('items__showing').all()
    serializer_class = BookingSerializer


class BookingItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddBookingItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateBookingItemSerializer
        return BookingItemSerializer
    
    def get_serializer_context(self):
        return {
            'booking_id': self.kwargs['booking_pk'],
            'request': self.request,
        }

    def get_queryset(self):
        return BookingItem.objects.filter(booking__id=self.kwargs['booking_pk'])


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # re-defining the queryset to be either admin or user associated can see the order
    def get_queryset(self):

        if self.request.user.is_authenticated:

            user = self.request.user

            if user.is_staff:
                return Order.objects.all()
            
            # (student_id, created) = Student.objects.only('id').get_or_create(user_id=user.id)
            student_id = Student.objects.only('id').get(user_id=user.id)
            return Order.objects.filter(student_id=student_id)
        
        return Order.objects.none()


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer