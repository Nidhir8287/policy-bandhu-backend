from django.urls import path
from .views import *

urlpatterns = [
    # 1 & 2: GET all chats, POST create new chat
    path('messages', MessageListAPIView.as_view(), name='chat-list'),

    # 4 (optional): GET messages in a chat
    path('send-messages/create', MessageCreateAPIView.as_view(), name='chat'),
]
