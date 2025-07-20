"""
URL configuration for gemini_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_auth.views import *
from subscriptions.views import *
from gemini_api.views import *

urlpatterns = [
    path('auth/signup/', UserSignup.as_view()),
    path('auth/send-otp/', SendOtp.as_view()),
    path('auth/verify-otp/', VerifyOTP.as_view()),
    path('auth/forgot-password/', ForgotPassword.as_view()),
    path('auth/change-password/',ChangePassword.as_view()),
    path('user/me/', UserDetails.as_view()),

    path('subscribe/pro/', ProSubscription.as_view()),
    path('webhook/stripe/', StripeWebhook.as_view()),
    path('subscription/status/', SubscriptionStatus.as_view()),
    path('payment/success/', PaymentSuccess.as_view()),

    path('chatroom/', ChatRoomCreatList.as_view()),
    path('chatroom/<int:id>/', ChatRoomDeleteDetail.as_view()),
    path('chatroom/<int:id>/message/', ChatMessageSendRecieve.as_view()),

]
