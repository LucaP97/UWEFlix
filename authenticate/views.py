from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

# Create your views here.
class UserViewSet(ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'cinema_manager') or self.request.user.is_staff:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()
        
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
