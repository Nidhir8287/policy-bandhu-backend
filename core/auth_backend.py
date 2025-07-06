# auth_backend.py
import requests
import jwt
from jwt import PyJWKClient
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

SUPABASE_PROJECT_ID = 'rzkpmikvcmxohlqofshv'  # e.g. abcdefghijklmnopqrstuvwxyz
SUPABASE_JWKS_URL = f'https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys'

class SupabaseJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            jwks_client = PyJWKClient(SUPABASE_JWKS_URL)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=None,  # Optional: use if you have audience in JWT
                options={"verify_exp": True},
            )
            # You can create/get Django user here
            user_id = decoded.get("sub")
            email = decoded.get("email")
            # ... fetch/create Django user
            return (YourUserModel.objects.get_or_create(email=email)[0], None)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid Supabase token: {str(e)}")
