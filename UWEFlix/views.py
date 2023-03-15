from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets
from .models import *
from .serializers import *
from decimal import Decimal

print("username: admin password: LMicyb8=O\n")

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

# films

class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def destroy(self, request, *args, **kwargs):
        if Showing.objects.filter(film_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Film cannot be deleted because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# screens
class ScreenViewSet(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

    

# showings
# only issue is showing_time doesnt appear in the default form
class ShowingViewSet(ModelViewSet):
    queryset = Showing.objects.select_related('film', 'screen').all()
    serializer_class = ShowingSerializer
    
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@api_view(['GET','POST'])
def booking_request(request,id):
    
    try:
        booking = Showing.objects.get(pk=id)
    except Showing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)        
        if serializer.is_valid():
            
            # get reference
            showing_ref = id
            # get ticket amount
            tkt_student_amnt = int(request.data.get('student'))
            tkt_adult_amnt = int(request.data.get('adult'))
            tkt_child_amnt = int(request.data.get('child'))
            
            global ticket_ref
            # create amount of tickets          
            if tkt_student_amnt != 0:
                for tickets in range(tkt_student_amnt):
                    tickets = Ticket.objects.create(
                        ticket_showing_ref = showing_ref,
                        ticket_type = 'Student',
                        ticket_price = '10', 
                        film = serializer.data['film'],
                        screen = serializer.data['screen'],
                        showing_time = serializer.data['showing_time'])
                    tickets.save()
                
            if tkt_adult_amnt != 0:
                for tickets in range(tkt_adult_amnt):
                    tickets = Ticket.objects.create(
                        ticket_showing_ref = showing_ref,
                        ticket_type = 'Adult',
                        ticket_price = '15', 
                        film = serializer.data['film'],
                        screen = serializer.data['screen'],
                        showing_time = serializer.data['showing_time'])
                    tickets.save()
            
            if tkt_child_amnt != 0:
                for tickets in range(tkt_child_amnt):
                    tickets = Ticket.objects.create(
                        ticket_showing_ref = showing_ref,
                        ticket_type = 'child',
                        ticket_price = '5', 
                        film = serializer.data['film'],
                        screen = serializer.data['screen'],
                        showing_time = serializer.data['showing_time'])
                    tickets.save()        
            
            total_ticket_price = Decimal((tkt_student_amnt * 10)+(tkt_adult_amnt * 15)+(tkt_child_amnt * 5))
            
            b = Booking.objects.create(
                showing_ref = showing_ref,
                film = request.data.get('film'),
                screen = request.data.get('screen'),
                showing_time = request.data.get('showing_time'),
                student = tkt_student_amnt,
                adult = tkt_adult_amnt,
                child = tkt_child_amnt,
                total_price = total_ticket_price
                )            
            b.save()
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
