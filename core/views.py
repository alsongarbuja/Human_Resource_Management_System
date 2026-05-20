from django.shortcuts import render

from punchmanagement.utils import get_employee_clock_status_context

def login(request):
  return render(request, "auth/login.html")

def dashboard(request):
  clock_status_context = get_employee_clock_status_context(request.user)

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
