from django.db import models

from core.models import BaseModel
from employeemanagement.models import JobProfile

class Notification(BaseModel):
  class Channel(models.TextChoices):
    IN_APP = 'IN_APP', 'In-App'
    EMAIL = 'EMAIL', 'Email'
    SMS = 'SMS', 'SMS'

  class Status(models.TextChoices):
    PENDING = 'PENDING', 'pending'
    SENT = 'SENT', 'Sent'
    FAILED = 'FAILED', 'Failed'

  recipient = models.ForeignKey(JobProfile, on_delete=models.CASCADE, related_name='notificatons')
  verb = models.CharField(max_length=255)
  channel = models.CharField(choices=Channel.choices, max_length=50, default=Channel.IN_APP)
  status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
  extra_data = models.JSONField(default=dict, blank=True)
  is_read = models.BooleanField(default=False)

  class Meta(BaseModel.Meta):
    db_table = "notification"
    verbose_name = "Notification"
    verbose_name_plural = "Notifications"
    ordering = ['-created_at']
    indexes = [
      models.Index(fields=['recipient', 'is_read']),
    ]
