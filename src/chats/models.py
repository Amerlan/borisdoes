from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    chat_name = models.CharField(max_length=40, unique=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class MessageHistoryLog(models.Model):
    class Meta:
        ordering = ["-created_at", ]
    sender = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True, db_index=True, blank=True,)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    @property
    def created_at_pretty(self):
        return f"{self.created_at.astimezone()}".split('.')[0]
