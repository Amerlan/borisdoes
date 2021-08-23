from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ChatSerializer, MessageHistoryLogSerializer
from .models import Chat, MessageHistoryLog
from .pagination import LimitOffsetPagination, get_paginated_response


class ChatApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = ChatSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class MessageApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, chat_name):
        chat = Chat.objects.get(chat_name=chat_name)
        messages = MessageHistoryLog.objects.filter(chat=chat).order_by('-created_at')
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=MessageHistoryLogSerializer,
            queryset=messages,
            request=request,
            view=self
        )
