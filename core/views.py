from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required

from employeemanagement.models import EmployeeProfile, JobProfile, ProfileTemplate
from punchmanagement.utils import get_employee_clock_status_context
from leavemanagement.utils import get_employee_time_off_requests_context

def login(request):
  """
    Render the login.html file when visiting the /auth/login path
  """
  return render(request, "auth/login.html")

def select_unit(request):
  """
    Render the unit-selection.html file when visiting /app/units path

    Also sends the list of units current employee is assigned if multiple present
    else redirects to dashboard page if only one unit or manager in all unit
  """
  employee_profile = get_object_or_404(EmployeeProfile, user=request.user)
  job_profiles = get_list_or_404(JobProfile, employee=employee_profile)

  if len(job_profiles) <= 1 or (all(p.profile_template.role.name == 'Manager' for p in job_profiles) and len({p.profile_template.unit.department_id for p in job_profiles}) == 1):
    request.session['active_unit_id'] = int(job_profiles[0].profile_template.unit.id)
    request.session['active_role_id'] = int(job_profiles[0].profile_template.role.id)
    return redirect("core:dashboard")

  context = {
    'units': job_profiles
  }

  return render(request, "app/unit-selection.html", context)

@login_required
def set_active_unit(request):
  """
  A intermediate view created simply to add the selected unit in the session
  After which it redirects to dashboard page
  """
  if request.method == "POST":
    selected_unit = request.POST.get("selected_unit")
    request.session['active_unit_id'] = int(selected_unit.split('-')[0])
    request.session['active_role_id'] = int(selected_unit.split('-')[1])
    return redirect("core:dashboard")

def dashboard(request):
  """
  Dashboard view when visiting /app/dashboard path
  """
  clock_status_context = get_employee_clock_status_context(request.user, request.active_unit)

  timeoff_requests = get_employee_time_off_requests_context(request.user, request.active_unit)

  context = {
    'total_hours_worked': '74.2',
    'regular_hours': '70.0',
    'ot_hours': '4.2',
  }

  context.update(clock_status_context)
  context.update(timeoff_requests)

  return render(request, "app/dashboard.html", context)
