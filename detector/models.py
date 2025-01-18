from django.db import models
from django.contrib.auth.models import User
class CallLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    call_log = models.TextField()
    confidence_level = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Call Log {self.timestamp} - Confidence: {self.confidence_level}%"

    class Meta:
        ordering = ['-timestamp']  # Most recent logs first 