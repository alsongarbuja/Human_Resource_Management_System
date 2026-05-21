from employeemanagement.models import EmployeeProfile, JobProfile
from punchmanagement.models import PunchEntry

def get_employee_clock_status_context(user, active_unit_id):
  """
    Reusable utility function to get the currently logged in employee's clock in status
  """

  if not user.is_authenticated:
    return {}

  try:
    employee_profile = EmployeeProfile.objects.get(user=user)
    job_profile = JobProfile.objects.get(employee=employee_profile, unit=active_unit_id)
  except (EmployeeProfile.DoesNotExist, JobProfile.DoesNotExist):
    return {
        'pay_period_start': "N/A",
        'pay_period_end': "N/A",
        'user_is_clocked_in': False,
        'clock_in_time': None,
        'unit': "N/A",
    }

  active_punch = PunchEntry.objects.filter(
    employee=employee_profile,
    job_profile=job_profile,
    clock_out__isnull=True
  ).order_by('-clock_in').first()

  context = {
    'pay_period_start': active_punch.pay_period.start_date if active_punch else "-",
    'pay_period_end': active_punch.pay_period.end_date if active_punch else "-",
    'user_is_clocked_in': active_punch is not None,
    'clock_in_time': active_punch.clock_in.strftime("%H:%M") if active_punch else None,
    'unit': active_unit_id.name,
  }

  return context
