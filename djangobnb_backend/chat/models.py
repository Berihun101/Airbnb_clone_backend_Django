from django.db import models
import uuid

# Create your models here.
from useraccount.models import User


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.id}'
    
class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages',)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    created_at = models.DateTimeField(auto_now_add=True)