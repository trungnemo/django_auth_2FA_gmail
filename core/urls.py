from django.urls import path
from .views import (RegisterAPIView, LoginAPIView, 
                    UserAPIView,RefreshAPIView,
                    LogoutAPIView,ForgotPasswordAPIView,
                    ResetPasswordAPIView)

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login',LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('forgotpassword', ForgotPasswordAPIView.as_view()),
    path('resetpassword',ResetPasswordAPIView.as_view())
]