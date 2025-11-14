from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.methods.auth import register_user, login_user

class RegisterView(APIView):
    def post(self, request):
        user, tokens = register_user(request.data)
        return Response({"user": user.username, "tokens": tokens}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user, tokens = login_user(username, password)
        if user:
            return Response({"user": user.username, "tokens": tokens}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
