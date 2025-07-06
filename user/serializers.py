"""
Serializes for the user API views
"""
from django.contrib.auth import (
    get_user_model,
    authenticate
)

from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import User, UserProfile
import user.utils as utils

"""
serializers are class that converts objects to and from
python objects. It takes in json input that is posted
from the API and validates as per validation rules.
Converts it to either and python objects or models
serializer.ModelSerializer -> converts to model
serializer.Serializer -> converts to python objets
"""

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

