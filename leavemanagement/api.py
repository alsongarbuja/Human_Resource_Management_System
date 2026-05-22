from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from ninja import Router, Schema, Form
from datetime import date
from typing import Optional

from notificationmanagement.utils import notify
from .models import PayCode, LeaveBalance, TimeoffRequest
from employeemanagement.models import JobProfile, ProfileTemplate

router = Router()

class TimeOffRequestSchema(Schema):
  start_date: date
  end_date: date
  leave_type: int
  reason: Optional[str] = None

@router.post("/time-off-request")
def time_off_reques(request, data: TimeOffRequestSchema = Form(...)):
    """
    Clocks in the authenticated employee if they don't have an active shift.
    """
    redirect_url = "leave:timeoffRequests"

    jp = get_object_or_404(JobProfile, employee__user=request.user, profile_template__unit=request.active_unit)

    try:
      pay_code = PayCode.objects.get(id=data.leave_type)
    except PayCode.DoesNotExist:
      messages.error(request, "Selected leave type is invalid.")
      return redirect(redirect_url)

    # balance_record = LeaveBalance.objects.filter(
    #   job_profile=jp,
    #   pay_code=pay_code,
    # ).first()

    # if not balance_record.balance:
    #   messages.error(request, f"You do not have an enough balance for {pay_code.name}.")
    #   return redirect(redirect_url)

    TimeoffRequest.objects.create(
      employee=jp,
      leave_type=pay_code,
      start_date=data.start_date,
      end_date=data.end_date,
      reason=data.reason
    )

    manager_profile_template = ProfileTemplate.objects.get(
      unit=jp.profile_template.unit,
      role__name="Manager"
    )
    manager_job_profiles = JobProfile.objects.filter(
      profile_template=manager_profile_template
    )

    for mjp in manager_job_profiles:
      notify(
        recipient=mjp,
        verb="An employee requested an time off!",
        # * Notifiy with email later on
      )

    messages.success(request, f"Successfully requested time off")
    return redirect(redirect_url)
