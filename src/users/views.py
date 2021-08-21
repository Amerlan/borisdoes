from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import login, authenticate, logout
from .serializers import LoginSerializer, RegisterSerializer


class RegisterApi(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class LoginApi(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        logout(request=request)
        return Response(status=status.HTTP_200_OK)
