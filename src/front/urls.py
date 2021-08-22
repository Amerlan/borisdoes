from django.urls import path
from .views import LoginPageApi, RegisterPageApi, ChatPageApi, ChatDetailPageApi

urlpatterns = [
    path('', LoginPageApi.as_view(), name='login'),
    path('signup/', RegisterPageApi.as_view(), name='signup'),
    path('chats/', ChatPageApi.as_view(), name='chat-list'),
    path('chats/<str:chat_id>/', ChatDetailPageApi.as_view(), name='chat'),
]
