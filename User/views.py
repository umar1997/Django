from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission, IsAdminUser

import jwt
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Person
from .utils import Email, IsOwnerOrReadOnly
from .serializers import (
    RegisterUserSerializer, 
    CustomTokenObtainPairSerializer, 
    ChangePasswordSerializer, 
    ProfileSerializer, 
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView



#### REGISTER USER
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#### CHANGE PASSWORD
# path('change_password/<str:pk>/', ChangePasswordView.as_view(), name='change_password'),
# class ChangePasswordView(generics.UpdateAPIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     queryset = Person.objects.all()
#     serializer_class = ChangePasswordSerializer

#### CHANGE PASSWORD
class ChangePasswordView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, id):
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return Response({'Error':'Profile Not Found'},status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format='json'):
        user = self.get_object(str(request.user.id))
        serializer= ChangePasswordSerializer(user, data=request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Success': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#### GET PROFILE
class ProfileView(generics.RetrieveUpdateDestroyAPIView, IsOwnerOrReadOnly):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Person.objects.all()
    serializer_class = ProfileSerializer


#### RETRIEVE TOKEN
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer



# RESET PASSWORD EMAIL
class RequestPasswordResetEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if Person.objects.filter(email=email).exists():
            user = Person.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse('User:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})

            # redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl # +"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Email.send_email(data)
            return Response({'Success': 'Reset Password Email Sent'}, status=status.HTTP_200_OK)
        # Take Response out of if statement
        # A person can't check whose email is in the database or not if every response is a success
        else:
            return Response({'Error': 'Email Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Person.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Error': 'Token is not valid anymore, Request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Success': 'Credentials are valid','uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'Error': 'Token is not valid anymore, Request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Success': 'Password Reset Successfully'}, status=status.HTTP_200_OK)