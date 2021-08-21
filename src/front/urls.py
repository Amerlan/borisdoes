from django.urls import path
from .views import LoginPageApi, RegisterPageApi

urlpatterns = [
    path('', LoginPageApi.as_view(), name='login'),
    path('signup/', RegisterPageApi.as_view(), name='signup'),
    # path('chats/', ),
    # path('chat/{str:chat_id}')
]
