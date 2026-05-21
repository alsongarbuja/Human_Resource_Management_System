from django.db import models

from core.models import BaseModel
from employeemanagement.models import EmployeeProfile, JobProfile

class PayCode(BaseModel):
  """
    This contains data about the type of paycode in the system

    Fields:
      - name: Char (Name of the pay code)
      - description?: Text (description of the pay code)
  """
  name = models.CharField(max_length=10, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "pay_code"
    verbose_name = "Pay Code"
    verbose_name_plural = "Pay Codes"

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
  """
  leave_type = models.ForeignKey(PayCode, on_delete=models.CASCADE)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  stauts = models.TextField(choices={
    'Requested': 'Requested',
    'Approved': 'Approved',
    'Rejected': 'Rejected',
  })
  employee = models.ForeignKey(EmployeeProfile, on_delete=models.PROTECT)

  def __str__(self):
    return f"Time of request by {self.employee.user.username}"

  class Meta(BaseModel.Meta):
    db_table = "timeoff_request"
    verbose_name = "Time off request"
    verbose_name_plural = "Time off requests"

# * Leave Balance Model
class LeaveBalance(BaseModel):
  """
    This model contains details about leave balance

    Fields:
      - pay_code: FK (connect with pay code)
      - balance: Float (actual balance)
      - job_profile: FK (connected job profile the balaance)
  """
  pay_code = models.ForeignKey(PayCode, on_delete=models.PROTECT)
  balance = models.FloatField(blank=False)
  job_profile = models.ForeignKey(JobProfile, on_delete=models.PROTECT)

  def __str__(self):
    return f'{self.job_profile.employee.user.username}:({self.pay_code}-{self.balance})'

  class Meta(BaseModel.Meta):
    db_table = "leave_balance"
    verbose_name = "Leave Balance"
    verbose_name_plural = "Leave Balances"
