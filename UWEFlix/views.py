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
from rest_framework import status
from .models import *
from .serializers import *

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
