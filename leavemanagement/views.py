from django.shortcuts import render

from .utils import get_employee_time_off_requests_context

def timeOffRequests(request):
  context = get_employee_time_off_requests_context(request.user, request.active_unit)

  return render(request, "leave/time-off-request.html", context)
