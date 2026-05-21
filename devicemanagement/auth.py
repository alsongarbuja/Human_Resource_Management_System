from ninja.security import APIKeyHeader
from django.http import HttpRequest
from .models import KioskToken

class KioskTokenAuth(APIKeyHeader):
  param_name = "X-Kiosk-Token"

  def authenticate(self, request: HttpRequest, key: str):
    try:
      token = KioskToken.objects.select_related('kiosk__user').get(
        key=key,
        is_active=True,
        kiosk__is_active=True
      )
      return token.kiosk.user
    except KioskToken.DoesNotExist:
      return None
