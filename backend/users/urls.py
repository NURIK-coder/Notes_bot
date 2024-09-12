from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserCreateApiView, GetCurrentUserAPIView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('register/', UserCreateApiView.as_view()),
    path('current_user/', GetCurrentUserAPIView.as_view())
]