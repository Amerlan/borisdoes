from django.urls import path
from .views import ChatApi, MessageApi


urlpatterns = [
    path('', ChatApi.as_view(), name='chats'),
    path('<str:chat_name>/messages/', MessageApi.as_view(), name='messages')
]
