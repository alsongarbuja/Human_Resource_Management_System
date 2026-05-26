from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from .utils import get_employee_clock_status_context

# @permission_required("")
def clockInOut(request):
  context = get_employee_clock_status_context(request.user, request.active_unit)

  return render(request, "punch/clock-in-out.html", context)

def scanClockInOut(request):

  return render(request, "punch/scan-clock-in-out.html")
