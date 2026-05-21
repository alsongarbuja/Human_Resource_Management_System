from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from employeemanagement.models import EmployeeProfile, JobProfile
from punchmanagement.utils import get_employee_clock_status_context

def login(request):
  return render(request, "auth/login.html")

def select_unit(request):
  employee_profile = EmployeeProfile.objects.get(user=request.user)
  job_profile = JobProfile.objects.filter(employee=employee_profile)

  jp = list(job_profile)

  if len(jp) <= 1:
    request.session['active_unit_id'] = int(job_profile[0].unit.id)
    return redirect("core:dashboard")

  if all(p.role.name == 'Manager' for p in jp) and len({p.unit.department_id for p in jp}) == 1:
    request.session['active_unit_id'] = int(job_profile[0].unit.id)
    return redirect("core:dashboard")

  context = {
    'units': jp
  }

  return render(request, "app/unit-selection.html", context)

@login_required
def set_active_unit(request):
  if request.method == "POST":
    selected_unit_id = request.POST.get("selected_unit_id")
    request.session['active_unit_id'] = int(selected_unit_id)
    return redirect("core:dashboard")

def dashboard(request):
  clock_status_context = get_employee_clock_status_context(request.user, request.active_unit)

  dummy_timeoff_requests = [
    {
      'type': 'Vacation Leave',
      'start_date': 'June 12, 2026',
      'end_date': 'June 15, 2026',
      'days': '4 Days',
      'status': 'Approved'
    },
    {
      'type': 'Medical / Sick Leave',
      'start_date': 'July 02, 2026',
      'end_date': 'July 03, 2026',
      'days': '1 Day',
      'status': 'Pending'
    },
    {
      'type': 'Personal Leave',
      'start_date': 'Aug 18, 2026',
      'end_date': 'Aug 18, 2026',
      'days': '0.5 Days',
      'status': 'Approved'
    }
  ]

  context = {
    'total_hours_worked': '74.2',
    'regular_hours': '70.0',
    'ot_hours': '4.2',

    # Pass the dummy array to the template
    'timeoff_requests': dummy_timeoff_requests,
  }

  context.update(clock_status_context)

  return render(request, "app/dashboard.html", context)
