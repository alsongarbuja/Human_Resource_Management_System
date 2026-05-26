from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from ninja import Router, Schema, Form
from ninja.errors import HttpError

from employeemanagement.models import JobProfile, EmployeeProfile
from punchmanagement.models import PunchEntry, PayPeriod

router = Router()

class ClockOutFormSchema(Schema):
  # TODO: think about shift note too
  shift_notes: str = None
  redirect_url: str = "punch:clockInOut"

@router.post("/clock-in")
def clock_in_employee(request, data: ClockOutFormSchema = Form(...)):
    """
    Clocks in the authenticated employee if they don't have an active shift.
    """
    redirect_url = data.redirect_url

    job_profile = get_object_or_404(JobProfile, employee__user=request.user, profile_template__unit=request.active_unit)

    already_clocked_in = PunchEntry.objects.filter(
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
      job_profile=job_profile,
      clock_in=timezone.now()
    )

    messages.success(request, f"Successfully clocked in at {punch.clock_in.strftime('%H:%M')}.")
    return redirect(redirect_url)

@router.post("/clock-out")
def clock_out_employee(request, data: ClockOutFormSchema = Form(...)):
  """
    Clocks out the employee of their currently clocked in status
  """

  redirect_url = data.redirect_url

  jobProfile = get_object_or_404(JobProfile, employee__user=request.user, profile_template__unit=request.active_unit)

  active_punch = PunchEntry.objects.filter(
    job_profile=jobProfile,
    clock_out__isnull=True
  ).order_by('-clock_in').first()

  if not active_punch:
    messages.error(request, "You have no active clock in right now")
    return redirect(redirect_url)

  active_punch.clock_out = timezone.now()
  active_punch.save()

  messages.success(
    request,
    f"Successfully clocked out at {active_punch.clock_out.strftime('%H:%M')}"
  )

  return redirect(redirect_url)

class ScanClockInOutSchema(Schema):
  so_id: str

@router.post("/scan-clock-in-out")
def clock_in_out_via_scan(request, data: ScanClockInOutSchema = Form(...)):
  try:
    employee_profile = get_object_or_404(EmployeeProfile, unique_id=data.so_id)
    job_profile = get_object_or_404(JobProfile, employee=employee_profile, profile_template__unit=request.active_unit)

    active_punch = PunchEntry.objects.filter(
      job_profile=job_profile,
      clock_out__isnull=True
    ).order_by('-clock_in').first()


    if not active_punch:
      today = timezone.now().date()
      current_pay_period = PayPeriod.objects.filter(
        start_date__lte=today,
        end_date__gte=today
      ).first()

      if not current_pay_period:
        raise HttpError(400, "Cannot clock in: No active pay period found for today's date.")

      punch = PunchEntry.objects.create(
        job_profile=job_profile,
        clock_in=timezone.now()
      )

      msg = f"Successfully clocked in at {punch.clock_in.strftime('%H:%M')}."
    else:
      active_punch.clock_out = timezone.now()
      active_punch.save()

      msg = f"Successfully clocked out at {active_punch.clock_out.strftime('%H:%M')}"

    messages.success(request, msg)
    return {"message": msg}
  except Exception as err:
    print(err)
