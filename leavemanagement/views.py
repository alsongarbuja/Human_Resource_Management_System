from django.shortcuts import render, get_object_or_404

from .utils import get_employee_time_off_requests_context
from .forms import TimeOffRequestForm

from employeemanagement.models import JobProfile

def timeOffRequests(request):
  context = get_employee_time_off_requests_context(request.user, request.active_unit)

  return render(request, "leave/time-off-request.html", context)

def addTimeoffRequests(request):
  jp = get_object_or_404(JobProfile, employee__user=request.user, profile_template__unit=request.active_unit)

  form_instance = TimeOffRequestForm(job_profile=jp)
  return render(request, "leave/time-off-add.html", {
    'form': form_instance,
  })
