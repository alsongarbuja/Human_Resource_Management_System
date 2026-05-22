from django.shortcuts import get_object_or_404

from employeemanagement.models import JobProfile
from leavemanagement.models import TimeoffRequest

def get_employee_time_off_requests_context(user, active_unit_id):
  """
    Reusable utility function to get the currently logged in employee's time off requests
  """

  if not user.is_authenticated:
    return {}

  try:
    job_profile = get_object_or_404(JobProfile, employee__user=user, profile_template__unit_id=active_unit_id)
  except (JobProfile.DoesNotExist):
    return {
      'timeoff_requests': [],
    }

  timeoff_requests = []

  if job_profile.profile_template.role.name == "Manager":
    employees = JobProfile.objects.filter(profile_template__unit_id=active_unit_id)
    timeoff_requests = TimeoffRequest.objects.filter(
      employee__in=employees
    ).order_by('-start_date')
  else:
    timeoff_requests = TimeoffRequest.objects.filter(
      employee__id=job_profile.id,
    ).order_by('-start_date')

  context = {
    'timeoff_requests': list(timeoff_requests),
  }

  return context
