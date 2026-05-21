from django.shortcuts import get_object_or_404

from employeemanagement.models import EmployeeProfile, JobProfile
from leavemanagement.models import TimeoffRequest

def get_employee_time_off_requests_context(user, active_unit_id):
  """
    Reusable utility function to get the currently logged in employee's time off requests
  """

  if not user.is_authenticated:
    return {}

  try:
    employee_profile = get_object_or_404(EmployeeProfile, user=user)
    job_profile = get_object_or_404(JobProfile, employee=employee_profile, unit=active_unit_id)
  except (EmployeeProfile.DoesNotExist, JobProfile.DoesNotExist):
    return {
      'timeoff_requests': [],
    }

  timeoff_requests = TimeoffRequest.objects.filter(
    employee=job_profile.id,
  ).order_by('-start_date')

  context = {
    'timeoff_requests': timeoff_requests,
  }

  return context
