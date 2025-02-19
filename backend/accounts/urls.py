from django.urls import path

from .views import UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name='accounts'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    #todo user profile load url

]
