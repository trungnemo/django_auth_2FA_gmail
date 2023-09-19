import datetime, random, string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .serializers import UserSerializer
from .models import User, UserToken, Reset
from .authentication import (create_access_token, create_refresh_token,
                             decode_access_token, decode_refresh_token, JWTAuthentication)

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data 
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('password does not match')
        
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()    
    
        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = get_object_or_404(User, email=email) #user = User.objects.filter(email=email).first()       
        if user is None:
            raise exceptions.AuthenticationFailed('invalid credential')    

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('invalid credential')   

        #JWT tokent
        access_token = create_access_token(user.id)
        refresh_token= create_refresh_token(user.id)
        
        #validate if the token is valid or not
        UserToken.objects.create(
            user_id= user.id,
            token= refresh_token,
            expired_at=  datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        )
        
        response = Response()
        response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
        response.data = {
            'token': access_token
        }
                
        return response

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication] #if authenticated then get can be executed

    def get(self, request):
        return Response(UserSerializer(request.user).data)



class RefreshAPIView(APIView):
    def post(self, request):
        #get refresh token'
        refresh_token = request.COOKIES.get('refresh_token')
        user_id = decode_refresh_token(refresh_token)
        #Validate if token is expired
        if not UserToken.objects.filter(
            user_id=user_id,
            token = refresh_token,
            expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')
        
        access_token = create_access_token(user_id)
        
        return Response({
            'access_token': access_token
        })

class LogoutAPIView(APIView):
    #authentication_classes = [JWTAuthentication] #if logout then get can be executed

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')        
        #UserToken.objects.filter(user_id=request.user.id).delete()
        UserToken.objects.filter(token=refresh_token).delete()
        
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message':'success',
        }
        return response

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        Reset.objects.create(
            email=email,
            token=token
        )
        
        url = 'http://localhost:8080/reset/' + token
        
        send_mail(
            subject='Reset your password',
            message='Clich here <a href="%s">hear</a> to reset your pasword' %url,
            from_email='django@gmail.com',
            recipient_list=[email]
        )
        
        return Response({
            'message':'sucess'
            })
    
class ResetPasswordAPIView(APIView):
    def post(self, request):
        data = request.data 
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('password does not match')
        
        reset_pwd = Reset.objects.filter(token=data['token']).first()
        if not reset_pwd:
            raise exceptions.APIException('Invalid link')
        
        user = User.objects.filter(email=reset_pwd.email).first()
        if not user:
            raise exceptions.APIException('User not found')

        user.set_password(data['password'])
        user.save()
        
        return Response({
            'message':'success'
        })