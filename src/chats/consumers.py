import asyncio
import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['chats']

    async def connect(self):
        await self.accept()
        print(self.scope)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data='hello')

