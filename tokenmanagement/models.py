import secrets
from django.db import models

from core.models import BaseModel
from organizationmanagement.models import Kiosk

class KioskToken(BaseModel):
  """
    This model contains the custom token for scoping

    Fields:
      - token: Char (JWT token)
      - validity: Char ('always', 'timed')
      - is_active: Bool (indicate if the token is active or not)
      - kiosk: Kiosk FK (connect with the Kiosk)
  """
  token = models.CharField(max_length=40, unique=True, primary_key=True)
  validity = models.CharField(max_length=10, choices=['ALWAYS', 'TIMED'])
  is_active = models.BooleanField(default=True, help_text="Uncheck this to revoke the access from this kiosk")
  kiosk = models.ForeignKey(Kiosk, on_delete=models.CASCADE)

  def __str__(self):
    return self.kiosk.name

  def save(self, *args, **kwargs):
    if not self.token:
      self.token = secrets.token_hex(20)
    return super().save(*args, **kwargs)

  class Meta(BaseModel.Meta):
    db_table = "kiosk_token"
    verbose_name = "Kiosk Token"
    verbose_name_plural = "Kiosk Tokens"
