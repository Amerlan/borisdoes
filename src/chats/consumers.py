import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import MessageHistoryLog, Chat
from chats.serializers import MessageHistoryLogSerializer
from chats.tasks import send_scheduled
from channels.db import database_sync_to_async
from asgiref.wsgi import sync_to_async
from datetime import datetime, timedelta


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
        json_data = json.loads(text_data)
        message = json_data.pop('message')
        username = self.scope["user"]
        is_anonymous = json_data.pop('is_anonymous', None)
        is_scheduled = json_data.pop('schedule', None)
        if is_anonymous is not None:
            is_anonymous = True
        if is_scheduled is not None:
            dt = datetime.strptime(is_scheduled, '%Y-%m-%dT%H:%M')
            dt = dt - timedelta(hours=6)
            await self.celery_task(username=username.username, message=message, dt=dt, is_anonymous=is_anonymous)
        else:
            message_log = await self.store_message(user=username, text=message, is_anonymous=is_anonymous)
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
    def store_message(self, user, text, is_anonymous) -> MessageHistoryLog:
        chat = Chat.objects.get(chat_name=self.chat_name)
        if is_anonymous:
            message_log = MessageHistoryLog(text=text, chat=chat)
        else:
            message_log = MessageHistoryLog(sender=user, text=text, chat=chat)
        message_log.save()
        return message_log

    @sync_to_async
    def serialize_message(self, message_log: MessageHistoryLog):
        serializer = MessageHistoryLogSerializer(message_log)
        return serializer.data

    async def celery_task(self, username, message, dt, is_anonymous):
        task = send_scheduled.apply_async(args=[self.chat_group, self.chat_name, username, message, is_anonymous], eta=dt)
        return task
