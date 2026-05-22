from .models import Notification
from .tasks import send_notification_task

def notify(recipient, verb, channel=Notification.Channel.IN_APP, extra_data=None):
  """
  Main developer-facing API to trigger a notification safely.
  """
  notification = Notification.objects.create(
    recipient=recipient,
    verb=verb,
    channel=channel,
    extra_data=extra_data or {}
  )

  send_notification_task.delay(notification.id)
  return notification
