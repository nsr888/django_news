from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    title = models.CharField(max_length=64, null=False)
    
    def __str__(self):
        return self.title

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=False)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.created) + " | " + str(self.message)

    class Meta:
        ordering = ['-created']
