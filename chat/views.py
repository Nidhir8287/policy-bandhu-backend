from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *
from .robofy_utils import *
from django.conf import settings
from django.db import transaction
from core.models import User, TempUser, UserProfile
import random
import datetime
from django.db.models import Q

class MessageListAPIView(APIView):
    """
    GET: list all messages where request.user is author.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get('chat_id')
        data = Message.objects.filter(Q(author=request.user) | Q(to=request.user)).order_by('-updated_at')[:30]
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageCreateAPIView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        content = data.get('content')
        chat_id = data.get('chat_id')

        if not content:
            return Response(
                {"detail": "Field 'content' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.is_authenticated:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            if not user_profile:
                return Response("Please login", status=status.HTTP_400_BAD_REQUEST)
            # if not user_profile.is_subscribed and user_profile.message_count > 10:
            #     return Response("Max chat attempts for unsubscribed user", status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     user_profile.message_count += 1
            #     user_profile.save()
        else:
            user = None
        # Wrap in transaction so both messages get created or none
        with transaction.atomic():
            # 1. Save user message
            if user:
                user_msg = Message.objects.create(content=content, author=user, to=User.objects.get(id=1))
            else:
                user_msg = Message.objects.create(content=content)

            # 2. Send to Dialogflow
            id_ = chat_id
            if not chat_id:
                id_ = ""
            session_id = id_
            response = call_robofy(content, session_id)
            id_, bot_reply_text = response['SessionId'], response['response']
            try:
                pass
            except Exception as e:
                # Optionally handle errors: you may still return user_msg or an error
                bot_reply_text = None
                bot_reply_text = 'Message Failed'
                # log exception

            # 3. Save bot reply if any
            bot_msg = None
            if bot_reply_text:
                bot_msg = Message.objects.create(content=bot_reply_text, author=User.objects.get(id=1), to=request.user)
        # Prepare response: include both messages or only the bot reply
        resp_data = {
            "user_message": MessageSerializer(user_msg).data,
            "chat_id": id_,
        }
        if bot_msg:
            resp_data["bot_reply"] = MessageSerializer(bot_msg).data

        return Response(resp_data, status=status.HTTP_201_CREATED)

