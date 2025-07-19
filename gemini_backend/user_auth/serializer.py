from rest_framework import serializers
from user_auth.models import UserModel

# 1. For full user data (e.g. registration or profile)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'email', 'name', 'mobile_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user
    
# 2. For sending OTP (only mobile number is required)
from rest_framework import serializers

class SendOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)



# 3. For verifying OTP (not directly tied to model)
class VerifyOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)

# 4. For changing password(required auth)
class ChangePaswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)

# 5. For resetting password (does not require auth)
class ForgotPasswordSerialzier(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10)