from django.urls import path
from .views import ChatApi


urlpatterns = [
    path('', ChatApi.as_view(), name='chats'),
]
