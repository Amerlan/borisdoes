import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import MessageHistoryLog, Chat
from chats.serializers import MessageHistoryLogSerializer
from channels.db import database_sync_to_async
from asgiref.wsgi import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group = f"chat_{self.chat_name}"

        await self.channel_layer.group_add(
            self.chat_group,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group,
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)['message']
        username = self.scope["user"]
        message_log = await self.store_message(user=username, text=message)
        data = await self.serialize_message(message_log=message_log)
        await self.channel_layer.group_send(
            self.chat_group,
            {
                'type': 'chat_message',
                'text': data['text'],
                'username': data['sender'],
                'time': data['created_at_pretty']
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(event)
        )

    @database_sync_to_async
    def store_message(self, user, text) -> MessageHistoryLog:
        chat = Chat.objects.get(chat_name=self.chat_name)
        message_log = MessageHistoryLog(sender=user, text=text, chat=chat)
        message_log.save()
        return message_log

    @sync_to_async
    def serialize_message(self, message_log: MessageHistoryLog):
        serializer = MessageHistoryLogSerializer(message_log)
        return serializer.data
