from django.utils import timezone

from .models import PunchEntry, PayPeriod
from employeemanagement.models import EmployeeProfile, JobProfile

def get_employee_clock_status_context(user, active_unit_id):
  """
    Reusable utility function to get the currently logged in employee's clock in status
  """

  if not user.is_authenticated:
    return {}

  pay_period = get_current_pay_period()

  try:
    job_profile = JobProfile.objects.get(employee__user=user, profile_template__unit_id=active_unit_id)
  except (EmployeeProfile.DoesNotExist, JobProfile.DoesNotExist):
    return {
        'pay_period_start': pay_period.start_date if pay_period else "N/A",
        'pay_period_end': pay_period.end_date if pay_period else "N/A",
        'user_is_clocked_in': False,
        'clock_in_time': None,
    }

  active_punch = PunchEntry.objects.filter(
    job_profile=job_profile,
    clock_out__isnull=True
  ).order_by('-clock_in').first()

  context = {
    'pay_period_start': pay_period.start_date if pay_period else "N/A",
    'pay_period_end': pay_period.end_date if pay_period else "N/A",
    'user_is_clocked_in': active_punch is not None,
    'clock_in_time': active_punch.clock_in if active_punch else None,
  }

  return context

def get_current_pay_period():
  today = timezone.now().date()
  print(today)
  pay_period = PayPeriod.objects.filter(
    start_date__lte=today,
    end_date__gte=today,
  ).first()

  if not pay_period:
    return None

  return pay_period
