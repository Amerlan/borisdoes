from channels import layers
from asgiref.sync import async_to_sync
from chats.serializers import MessageHistoryLogSerializer
from conf.celery import celery_app
from .models import Chat, MessageHistoryLog
from django.contrib.auth.models import User


@celery_app.task
def send_scheduled(group_chat, chat_name, username, message, is_anonymous):
    chat = Chat.objects.get(chat_name=chat_name)
    if not is_anonymous:
        user = User.objects.get(username=username)
        message_log = MessageHistoryLog(sender=user, text=message, chat=chat)
    else:
        message_log = MessageHistoryLog(text=message, chat=chat)
    message_log.save()
    serializer = MessageHistoryLogSerializer(message_log)
    validated_data = serializer.data
    channel_layer = layers.get_channel_layer()
    async_to_sync(
        channel_layer.group_send
    )(group_chat, {
        'type': 'chat_message',
        'room_group_name': group_chat,
        'text': validated_data['text'],
        'username': validated_data['sender'],
        'time': validated_data['created_at_pretty']

    })


