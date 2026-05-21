import secrets
from django.db import models

from core.models import BaseModel
from organizationmanagement.models import Department

class Kiosk(BaseModel):
  """
    This model contains details about the kiosk/devices linked to the department

    Fields:
      - user: FK (connect to user)
      - department: FK (connection to department model)
      - name: Char (a unique name for the device)
      - description: TextField (a description of the kiosk)
      - allowedIP: Ip Address (a allowed ip address from which the kiosk can send request)
  """
  user = models.ForeignKey(
    "auth.User", on_delete=models.PROTECT,
  )
  department = models.ForeignKey(
    Department, on_delete=models.PROTECT,
  )
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)
  allowedIP = models.GenericIPAddressField(unique=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "kiosk"
    verbose_name = "Kiosk Device"
    verbose_name_plural = "Kiosk Devices"

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
  validity = models.TextField(max_length=10, choices={
    'ALWAYS': 'Always',
    'TIMED': 'Timed',
    })
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
