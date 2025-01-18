from django.db import models

class CallAnalysis(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_scam = models.BooleanField()
    confidence = models.FloatField()
    warning_signs = models.JSONField()

    class Meta:
        verbose_name_plural = "Call analyses"

    def __str__(self):
        return f"Call Analysis at {self.timestamp}" 