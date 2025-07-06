from django.db import models
from core.models import User
from django.utils import timezone

class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    conversation_id = models.CharField(max_length=512)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        if self.author:
            auth = self.author.email
        else:
            auth = 'anon'
        return f"[{self.updated_at:%Y-%m-%d %H:%M}] {auth}: {self.content[:20]}"