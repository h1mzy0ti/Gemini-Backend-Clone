# gemini_backend/middleware.py

import jwt
from django.conf import settings
from django.http import JsonResponse
from user_auth.models import UserModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        public_paths = [
            '/auth/signup/', '/auth/send-otp/', '/auth/verify-otp',
            '/auth/forgot-password/','/webhook/stripe/','/payment/success/'
        ]

        if any(path.startswith(p) for p in public_paths):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization token missing'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = UserModel.objects.get(id=payload['user_id'])
            request.user = user
        except (ExpiredSignatureError, InvalidTokenError):
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return self.get_response(request)
