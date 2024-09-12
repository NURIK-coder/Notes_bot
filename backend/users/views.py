from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.serializers import UserCreateSerializer, UserSerializer


# Create your views here.


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class GetCurrentUserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = None

