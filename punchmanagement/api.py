from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from ninja import Router, Form
from ninja.errors import HttpError

from employeemanagement.models import EmployeeProfile, JobProfile
from punchmanagement.models import PunchEntry, PayPeriod

router = Router()

@router.post("/clock-in")
def clock_in_employee(request, data: str = Form(None)):
    """
    Clocks in the authenticated employee if they don't have an active shift.
    """
    redirect_url = "punch:clockInOut"

    employee_profile = get_object_or_404(EmployeeProfile, user=request.user)
    job_profile = get_object_or_404(JobProfile, employee=employee_profile)

    already_clocked_in = PunchEntry.objects.filter(
      employee=employee_profile,
      job_profile=job_profile,
      clock_out__isnull=True
    ).exists()

    if already_clocked_in:
      raise HttpError(400, "You are already clocked in.")

    today = timezone.now().date()
    current_pay_period = PayPeriod.objects.filter(
      start_date__lte=today,
      end_date__gte=today
    ).first()

    if not current_pay_period:
      raise HttpError(400, "Cannot clock in: No active pay period found for today's date.")

    punch = PunchEntry.objects.create(
      employee=employee_profile,
      job_profile=job_profile,
      pay_period=current_pay_period,
      # TODO: fix this timezone
      clock_in=timezone.now()
    )

    messages.success(request, f"Successfully clocked in at {punch.clock_in.strftime('%H:%M')}.")
    return redirect(redirect_url)
