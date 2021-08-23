from rest_framework import serializers
from .models import Chat, MessageHistoryLog


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'chat_name',
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        chat = Chat(creator=user, **validated_data)
        chat.save()
        return chat


class MessageHistoryLogSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = MessageHistoryLog
        fields = (
            'sender', 'text', 'created_at_pretty'
        )

    def get_sender(self, obj):
        if obj.sender:
            return obj.sender.username
        return 'Anonymous User'
