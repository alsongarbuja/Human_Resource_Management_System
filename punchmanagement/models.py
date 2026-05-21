from django.db import models
from django.conf import settings
from django.utils import timezone

import pytz
from datetime import timedelta, datetime, time

from core.models import BaseModel
from employeemanagement.models import EmployeeProfile, JobProfile

# * Pay Period Model
class PayPeriod(BaseModel):
  """
    This contains the auto generated Pay Period for the system

    Fields:
      - start_date: DateTime (Start of the pay period)
      - end_date: DateTime (End of the pay period)
  """
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()

  class Meta(BaseModel.Meta):
    db_table = "pay_period"
    verbose_name = "Pay Period"
    verbose_name_plural = "Pay Periods"

  @classmethod
  def generate_pay_period_bi_weekly(self, num_of_periods=30, start_from_date=None):
    """
      Auto generate biweekly pay period in the system
    """
    if num_of_periods <= 0:
      return 0, None

    local_tz = pytz.timezone(settings.TIME_ZONE)

    effective_start_local_dt = None
    latest_pay_period = self.objects.order_by("-end_date").first()

    if start_from_date:
      if timezone.is_naive(start_from_date):
        effective_start_local_dt = local_tz.localize(
          start_from_date.replace(hour=0, minute=0, second=0, microsecond=0)
        )
      else:
        effective_start_local_dt = start_from_date.astimezone(local_tz).replace(
          hour=0, minute=0, second=0, microsecond=0
          )
    elif latest_pay_period:
      latest_end_date_local = latest_pay_period.end_date.astimezone(
        local_tz
      ).date()
      next_start_date_component = latest_end_date_local + timedelta(days=1)
      effective_start_local_dt = local_tz.localize(
        datetime.combine(next_start_date_component, time(0, 0, 0))
      )
    else:
      effective_start_local_dt = local_tz.localize(datetime(2025, 2, 9, 0, 0, 0))

    created_count = 0
    current_start_local_dt = effective_start_local_dt
    initial_generated_start_utc = None

    for i in range(num_of_periods):
      current_end_date_component = current_start_local_dt.date() + timedelta(
        days=13
      )

      try:
        current_end_local_dt = local_tz.localize(
          datetime.combine(current_end_date_component, time(23, 59, 59))
        )
      except pytz.AmbiguousTimeError:
        current_end_local_dt = local_tz.localize(
          datetime.combine(current_end_date_component, time(23, 59, 59)),
          is_dst=True,
        )
      except pytz.NonExistentTimeError:
        next_day_midnight = local_tz.localize(
            datetime.combine(
                current_end_date_component + timedelta(days=1), time(0, 0, 0)
            )
        )
        current_end_local_dt = next_day_midnight - timedelta(seconds=1)

      start_date_utc = current_start_local_dt.astimezone(pytz.utc)
      end_date_utc = current_end_local_dt.astimezone(pytz.utc)

      if (self.objects.filter(
          start_date__lte=end_date_utc, end_date__gte=start_date_utc
        ).exclude(
          pk__in=self.objects.filter(start_date=start_date_utc, end_date=end_date_utc)
            ).exists()
      ):
        print(f"Overlap detected for period {start_date_utc} to {end_date_utc}. Stopping generation.")
        break

      self.objects.create(start_date=start_date_utc, end_date=end_date_utc)

      if initial_generated_start_utc is None:
        initial_generated_start_utc = start_date_utc

      created_count += 1
      next_start_date_component = current_end_local_dt.date() + timedelta(days=1)
      current_start_local_dt = local_tz.localize(
        datetime.combine(next_start_date_component, time(0, 0, 0))
      )

    return created_count, initial_generated_start_utc

# * Punch Entry Model
class PunchEntry(BaseModel):
  """
    This contains the punch entry data of employee

    Fields:
      - employee: FK (connected employee profile)
      - job_profile: FK (connected job profile)
      - clock_in: DateTime (Timestamp of clock in)
      - clock_out: DateTime (Timestamp of clock out)
      - ip_address?: IPAddress (Ip address of the clock in/out machine)
      - pay_period: FK (connected pay period)
  """
  employee = models.ForeignKey(EmployeeProfile, on_delete=models.PROTECT)
  job_profile = models.ForeignKey(JobProfile, on_delete=models.PROTECT)
  pay_period = models.ForeignKey(PayPeriod, on_delete=models.SET_NULL, null=True)

  clock_in = models.DateTimeField(db_index=True)
  clock_out = models.DateTimeField(null=True, blank=True, db_index=True)

  ip_address = models.GenericIPAddressField(blank=True, null=True)

  def __str__(self):
    status = "Active" if not self.clock_out else f"Ended at {self.clock_out.strftime('%H:%M')}"
    return f"{self.employee} ({self.job_profile.unit}) | {status}"

  class Meta(BaseModel.Meta):
    db_table = "punch_entry"
    verbose_name = "Punch Entry"
    verbose_name_plural = "Punch Entries"

    indexes = [
      models.Index(fields=["employee", "-clock_in"])
    ]
