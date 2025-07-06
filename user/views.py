"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import datetime

import user.utils as utils
from core.models import User, UserProfile
from user.serializers import (
    UserProfileSerializer
)

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def post(self, request):
        # Get or create the UserProfile for the authenticated user
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Update subscription fields
        user_profile.is_subscribed = True  # Assuming typo is fixed
        user_profile.expires_at = timezone.now() + timedelta(days=30)
        user_profile.save()
        
        # Serialize and return the updated profile
        serializer = self.serializer_class(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

