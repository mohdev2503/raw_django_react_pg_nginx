# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import pandas as pd
class UserCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#todo user profile edit view
#todo user profile load view

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_user_data(request):
    user = request.user  # This will be the authenticated user based on the token
    return Response({'username': user.username, 'email': user.email})