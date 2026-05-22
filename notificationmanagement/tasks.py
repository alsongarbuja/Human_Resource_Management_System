from celery import shared_task
from django.core.mail import send_mail
from .models import Notification

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification_task(self, notification_id):
  try:
    notification = Notification.objects.get(id=notification_id)

    if notification.channel == Notification.Channel.EMAIL:
      send_mail(
        subject="HR System Notification",
        message=f"Hello, someone {notification.verb}.",
        from_email="noreply@company.com",
        recipient_list=[notification.recipient.email],
        fail_silently=False,
      )

    elif notification.channel == Notification.Channel.IN_APP:
      pass

    notification.status = Notification.Status.SENT
    notification.save()

  except Exception as exc:
    notification.status = Notification.Status.FAILED
    notification.save()
    raise self.retry(exc=exc)
