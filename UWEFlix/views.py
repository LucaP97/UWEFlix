from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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
class FilmList(APIView):
    def get(self, request):
        queryset = Film.objects.all()
        serializer = FilmSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FilmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FilmDetail(APIView):
    def get(self, request, id):
        film = get_object_or_404(Film, pk=id)
        serializer = FilmSerializer(film)
        return Response(serializer.data)
    
    def put(self, request, id):
        film = get_object_or_404(Film, pk=id)
        serializer = FilmSerializer(film, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        film = get_object_or_404(Film, pk=id)
        if film.showing.count() > 0:
            return Response({'error': 'Film cannot be deleted because it has a showing associated with it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# screens
class ScreenList(APIView):
    def get(self, request):
        queryset = Screen.objects.all()
        serializer = ScreenSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ScreenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ScreenDetail(APIView):
    def get(self, request, id):
        screen = get_object_or_404(Screen, pk=id)
        serializer = ScreenSerializer(screen)
        return Response(serializer.data)
    
    def put(self, request, id):
        screen = get_object_or_404(Screen, pk=id)
        serializer = ScreenSerializer(screen, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        screen = get_object_or_404(Screen, pk=id)
        screen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# showings
class ShowingList(APIView):
    def get(self, request):
        queryset = Showing.objects.select_related('film', 'screen').all()
        serializer = ShowingSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ShowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ShowingDetail(APIView):
    def get(self, request, id):
        showing = get_object_or_404(Showing, pk=id)
        serializer = ShowingSerializer(showing)
        return Response(serializer.data)
    
    def put(self, request, id):
        showing = get_object_or_404(Showing, pk=id)
        serializer = ShowingSerializer(showing, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        showing = get_object_or_404(Showing, pk=id)
        showing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)