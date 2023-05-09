from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import stripe
from .models import *
from .serializers import *
from .filters import *
from .permissions import *


# user check
class CheckUserView(APIView):
    def get(self, request):
        if request.user.is_staff:
            return Response({'user': 'is_staff'})
        elif hasattr(request.user, 'cinema_manager'):
            return Response({'user': 'cinema_manager'})
        elif hasattr(request.user, 'clubrepresentative'):
            return Response({'user': 'club_representative'})
        elif hasattr(request.user, 'student'):
            return Response({'user': 'student'})
        elif hasattr(request.user, 'employee'):
            return Response({'user': 'employee'})
        elif hasattr(request.user, 'accountmanager'):
            return Response({'user': 'account_manager'})
        elif not request.user.is_authenticated:
            return Response({'user': 'guest'})
        else:
            return Response({'user': 'anonymous'})

# student
class StudentViewSet(ModelViewSet):
    # queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'cinema_manager') or self.request.user.is_staff:
            return Student.objects.all()
        else:
            return Student.objects.filter(user_id=self.request.user.id)
        
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentRegistrationSerializer
        if self.request.method == 'PUT':
            return StudentUpdateSerializer
        return StudentRegistrationSerializer

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
        
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            created_student = Student.objects.get(pk=response.data['id'])
            user = created_student.user

            try:
                message = BaseEmailMessage(
                    template_name = 'emails/student_registration.html',
                    context={'user': user}
                )
                message.send([user.email])
            except BadHeaderError:
                pass

        return response
        

class CinemaManagerViewSet(ModelViewSet):
    queryset = CinemaManager.objects.all()
    serializer_class = CinemaManagerRegistrationSerializer

    permission_classes = [IsStaffOrCinemaManager]


class TemporaryCinemaManagerViewSet(ModelViewSet):
    queryset = CinemaManager.objects.filter(expiration_date__isnull=False)
    serializer_class = TemporaryCinemaManagerRegistrationSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = RegisterEmployeeSerializer


# films
class FilmViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    
    queryset = Film.objects.prefetch_related('images').filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateFilmSerializer
        return FilmSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'short_trailer_description']

    # def destroy(self, request, *args, **kwargs):
    #     if Showing.objects.filter(film_id=kwargs['pk']).count() > 0:
    #         return Response({'error': 'Film cannot be deleted because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        is_active = request.data.get('is_active')
        if is_active is None or is_active == False:
            film_id = kwargs['pk']
            future_showings_count = Showing.objects.filter(film_id=film_id, showing_date__gte=timezone.now().date()).count()
            if future_showings_count > 0:
                return Response({'error': 'Film cannot be archived because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().update(request, *args, **kwargs)
    
    permission_classes = [IsCinemaManagerOrReadOnly]
    
    

class ArchivedFilmViewSet(ModelViewSet):
    http_method_names = ['get', 'put']

    queryset = Film.objects.prefetch_related('images').filter(is_active=False)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateFilmSerializer
        return FilmSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'short_trailer_description']

    permission_classes = [IsCinemaManagerOnly]


    
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
class ShowingViewSet(ModelViewSet):
    queryset = Showing.objects.select_related('film', 'screen', 'price').all()
    serializer_class = ShowingSerializer
        

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ShowingFilter
    search_fields = ['film__title']
    permission_classes = [IsCinemaManagerOrReadOnly]


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
    http_method_names = ['get', 'post', 'patch', 'put', 'delete', 'head', 'options']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        elif self.request.method == 'PUT':
            return CancelOrderSerializer
        return OrderSerializer

    # re-defining the queryset to be either admin or user associated can see the order
    def get_queryset(self):

        if self.request.user.is_authenticated:

            user = self.request.user

            if user.is_staff or hasattr(user, 'cinema_manager'):
                return Order.objects.filter(is_active=True)
            
            # (student_id, created) = Student.objects.only('id').get_or_create(user_id=user.id)
            student_id = Student.objects.only('id').get(user_id=user.id)
            return Order.objects.filter(student_id=student_id, is_active=True)
        
        return Order.objects.none()
    
    def create(self, request, *args, **kwargs):
        # # def stripe_payment(stripe):
        # public = 'pk_test_51N2bKfFHp8PAiHwAlHmLWQUwu8Q8uoikyJ1ljYTzkwjvhRsm5sgzvdZkDRjAn0E0so69mGEVX3tTZwH0L4oLH7PO00zVmmFcOg'
        # stripe.api_key = 'sk_test_51N2bKfFHp8PAiHwAYmXYVzUpnX8nodGWNN1ppgjYuEmsxwEaijATGGS0uHpnDVTW0iftRln4OVLlt7JNCrOHoexD003brCcnkH'

        # customer = stripe.Customer.create(email=self.request.user.email)
        # payment_data = {'customer': customer['id']}

        # session = stripe.checkout.Session.create(
        #     payment_method_types=['card'],
        #     line_items=[{
        #         'price_data': {
        #             'currency': 'gbp',
        #             'product_data': {
        #                 'name': 'Account top up',
        #                 'description': 'Quanity',
        #             },
        #             'unit_amount':  100,
        #         },
        #         'quantity': 1,
        #     }],
        #     mode='payment',
        #     success_url='https://example.com/success',
        #     cancel_url='https://example.com/cancel',
        # )

        # render(request, 'UWEFlix/stripe.html', {'session_id': session.id})
        
        # stripe_payment(stripe)


        # context = {'user': self.request.user, 'session_id': session.id} if self.request.user.is_authenticated else {'session_id': session.id}
        context = {'user': self.request.user} if self.request.user.is_authenticated else {}

        serializer = CreateOrderSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)

        response = Response(serializer.data)

        if response.status_code == 200 and self.request.user.is_authenticated:
            try:
                message = BaseEmailMessage(
                    template_name = 'emails/order_confirmation.html',
                    context={'user': self.request.user, 'order': order, 'total_price': serializer.data['total_price']}
                )
                message.send([self.request.user.email])
            except BadHeaderError:
                pass

        return response



    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]



class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderCancellationViewSet(ModelViewSet):
    http_method_names = ['get', 'put']

    queryset = OrderCancellationRequest.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateOrderCancellationSerializer
        return OrderCancellationSerializer
    

class ArchivedOrderViewSet(ModelViewSet):
    http_method_names = ['get']

    serializer_class = OrderSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated:

            user = self.request.user

            if user.is_staff or hasattr(user, 'cinema_manager'):
                return Order.objects.filter(is_active=False)
            
            # (student_id, created) = Student.objects.only('id').get_or_create(user_id=user.id)
            student_id = Student.objects.only('id').get(user_id=user.id)
            return Order.objects.filter(student_id=student_id, is_active=False)
        
        return Order.objects.none()
    



class PriceViewSet(ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer