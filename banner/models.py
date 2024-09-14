import uuid
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)


class Message(models.Model):
    text = models.TextField(null=True, blank=True)
    external_photo_id = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='images/', storage=default_storage)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField('Message', related_name="chats", through='ChatMessage')


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('chat', 'message')
