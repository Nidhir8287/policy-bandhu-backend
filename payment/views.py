# views.py
import razorpay
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, ValidationError
from django.views.decorators.csrf import csrf_exempt
from core.models import UserProfile

from .models import Payment, Coupon
from .serializers import PaymentSerializer

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        payload = request.data
        user = request.user
        payment, created = Payment.objects.get_or_create(
            name=payload['name'],
            email=payload['email'],
            phone=payload['phone'],
            screenshot=payload['screenshot'],
            message=payload['message'],
            user=request.user)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.pending_subscription=True
        user_profile.save()
        return Response('Order Created', status=status.HTTP_201_CREATED)