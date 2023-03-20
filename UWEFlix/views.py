from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import *
from .permissions import *

def home(request):
    
    name = "UWEFlix"

    return render(request, 'UWEFlix/home.html', {
        'name': name
    })

##################################################################################
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("there was an error logging in, please try again"))
            return redirect('login')
    else:
        return render(request, 'UWEFlix/login.html', {})
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}')
            return redirect('home')
        else: 
            messages.success(request, ("There was an error creating an account, please try again"))
            return redirect('register_user')
    else:
        form = UserCreationForm()
    return render(request, 'UWEFlix/register_user.html', {'form': form})


def logout_user(request):
    logout(request)
    if not request.user.is_authenticated:
        messages.success(request, "You have been logged out")
    else:
        messages.error(request, "unable to log you out")
    return redirect('home')
##################################################################################

# customer
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# films
class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = FilmFilter
    search_fields = ['title', 'short_trailer_description']

    def destroy(self, request, *args, **kwargs):
        if Showing.objects.filter(film_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Film cannot be deleted because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# screens
class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

    filter_backends = [SearchFilter]
    search_fields = ['screen_name']

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
    permission_classes = [IsAdminOrReadOnly]

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
        return {'booking_id': self.kwargs['booking_pk']}

    def get_queryset(self):
        return BookingItem.objects.filter(booking__id=self.kwargs['booking_pk'])
