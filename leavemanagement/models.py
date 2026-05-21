from django.db import models

from core.models import BaseModel

class LeaveType(BaseModel):
  """
    This contains data about the type of leave in the system

    Fields:
      - name: Char (Name of the leave type)

  """

# * Time off request Model
class TimeoffRequest(BaseModel):
  """
    This contains data about timeoff request

    Fields:
      - leave_type: FK (Type of leave)
      - start_date: DateTime (Start date of the leave request)
      - end_date: DateTime (End date of the leave request)
      - status: Char (Status of the time off request)
      - employee: FK (Employee who is requesting the leave)
      - job_profile: FK (The job profile of the employee requesting the leave)
      - approver: FK (Manager/Supervisor to approve the request by)

  """

  class Meta(BaseModel.Meta):
    db_table = "timeoff_request"
    verbose_name = "Time off request"
    verbose_name_plural = "Time off requests"
