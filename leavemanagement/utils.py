from employeemanagement.models import EmployeeProfile, JobProfile
from leavemanagement.models import TimeoffRequest

def get_employee_time_off_requests_context(user, active_unit_id):
  """
    Reusable utility function to get the currently logged in employee's time off requests
  """

  if not user.is_authenticated:
    return {}

  try:
    employee_profile = EmployeeProfile.objects.get(user=user)
    job_profile = JobProfile.objects.get(employee=employee_profile, unit=active_unit_id)
  except (EmployeeProfile.DoesNotExist, JobProfile.DoesNotExist):
    return {
      'timeoff_requests': [],
    }

  timeoff_requests = TimeoffRequest.objects.filter(
    employee=job_profile,
  ).order_by('-start-date')

  context = {
    'timeoff_requests': list(timeoff_requests),
  }

  return context
