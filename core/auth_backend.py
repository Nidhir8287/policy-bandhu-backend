# auth_backend.py
import requests
import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.models import User

SUPABASE_PROJECT_ID = 'rzkpmikvcmxohlqofshv'  # e.g. abcdefghijklmnopqrstuvwxyz
SUPABASE_JWKS_URL = f'https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys'

class SupabaseJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256'],
                audience='authenticated',
                issuer='https://rzkpmikvcmxohlqofshv.supabase.co/auth/v1'
            )
            # ... fetch/create Django user
            user_metadata = payload['user_metadata']
            user, created = User.objects.get_or_create(sub=user_metadata['sub'],
                                defaults={
                                    'name': user_metadata['name'],
                                    'email': user_metadata['email'],
                                    'picture': user_metadata['picture']
                                }
                            )
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid Supabase token: {str(e)}")
