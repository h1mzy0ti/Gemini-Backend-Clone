from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions  import IsAuthenticated
from user_auth.serializer import *
import random
from user_auth.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken


# In-memory storage (Optionally can use Redis or DB)
otp_store = {}


# Function to generate and "send" OTP
def GenerateOtp(user_number: str, otp_type: str = "login"):
    otp = str(random.randint(100000, 999999))
    otp_store[user_number] = otp
    otp_store[f"{user_number}_type"] = otp_type  # Store purpose alongside OTP
    return otp

# User signup view
class UserSignup(APIView):
    def post(self,request):

        userdata = UserSerializer(data=request.data)
        
        if userdata.is_valid():
              userdata.save()
              return Response({'message':'User Registered','user': userdata.data},status=status.HTTP_201_CREATED)
        return Response({'message':'User not Registered','error': userdata.errors}, status=status.HTTP_400_BAD_REQUEST)

# Send OTP to a mobile number (acts as a login system)
class SendOtp(APIView):
    def post(self, request):

        serializer = SendOtpSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            password = serializer.validated_data['password']

            try:
                user = UserModel.objects.get(mobile_number=mobile_number)
            except UserModel.DoesNotExist:
                return Response({'message': 'Mobile number not registered'}, status=status.HTTP_404_NOT_FOUND)

            if user.check_password(password):
                otp = GenerateOtp(str(mobile_number),otp_type="login")
                return Response({
                    'message': 'OTP sent',
                    'otp': otp  
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Invalid input', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Verify OTP endpoint
class VerifyOTP(APIView):
    def post(self,request):
        serializer = VerifyOtpSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = serializer.validated_data['otp']

            expected_otp = otp_store.get(mobile_number)
            otp_type = otp_store.get(f"{mobile_number}_type")

            if expected_otp == otp:
                user = get_object_or_404(UserModel, mobile_number=mobile_number)
                refresh = RefreshToken.for_user(user)

                # Removing the OTP after validation
                otp_store.pop(mobile_number, None)
                otp_store.pop(f"{mobile_number}_type", None)

                response_data = {
                    'message': 'OTP Verified',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }

                if otp_type == 'forgot_password':
                    response_data['next_step'] = '/auth/change-password'
                    response_data['note'] = 'Use access token to call /auth/change-password to set a new password.'

                return Response(response_data, status=status.HTTP_200_OK)
    
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


        return Response({'message': 'Invalid Data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# Forgot-password view for non Authenticated user( validates with mobile_number and otp)
class ForgotPassword(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerialzier(data=request.data)

        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']

            try: 
                user = UserModel.objects.get(mobile_number=mobile_number)
            except UserModel.DoesNotExist:
                return Response({'message':'Mobile number not registered'},status=status.HTTP_404_NOT_FOUND)

            if user:
                otp = GenerateOtp(str(mobile_number),otp_type="forgot_password")
                return Response({
                    'message' : 'Otp sent Please verify it for reseting password',
                    'otp' : otp
                }, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            
        
# Change password view
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePaswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']


            # Check current user from JWT session
            user = request.user
            serialize = UserSerializer(user)

            user.set_password(new_password)
            user.save()

            return Response({
                'message': ' Password changed',
                'user' : serialize.data
                })
        
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            

# Fetch current user details
class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):

        user = request.user
        serializer = UserSerializer(user)


        return Response({
            'message':'success',
            'Current user details': serializer.data
            
            },status=status.HTTP_200_OK)
    