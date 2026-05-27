import os
import datetime
from django.db import models
from django.core.validators import FileExtensionValidator

from core.models import BaseModel
from employeemanagement.models import JobProfile

class LeaveType(BaseModel):
  """
    Types of leave in the system

    Fields:
      - code: Char (code of the leave type)
      - name: Text (full name of the leave type)
      - parent_leave_type?: FK (self-referencing FK, Nullable denoting parent type)
      - overflow_leave_type?: FK (self-referencing FK, Nullable denoting any overflowing leave type)
  """
  code = models.CharField(max_length=5, unique=True)
  name = models.CharField(max_length=50)
  parent_leave_type = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="sub_type",
  )
  overflow_leave_type = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="overflow_to_type",
  )

  def __str__(self):
    return self.code

  class Meta(BaseModel.Meta):
    db_table = "leave_type"
    verbose_name = "Leave Type"
    verbose_name_plural = "Leave Types"

class LeaveConfiguration(BaseModel):
  """
    Different configuration of leave types

    Fields:
      - type: FK (leave of type)
      - initial_balance: Decimal (default to 0.0)
      - max_balance_cap?: Decimal (maximum balance cap)
      - max_hours_per_request?: Decimal (hours per request)
      - max_days_per_request?: Int (days per request)
      - max_requests_per_year?: Int (max times the request can be done for this type)
      - requires_documentation: boolean (indicate if documentation is required or not)
  """
  type = models.ForeignKey(
    LeaveType,
    on_delete=models.PROTECT,
    related_name="leave_configuration"
  )
  initial_balance = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=0.0,
  )
  max_balance_cap = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    null=True,
    blank=True,
  )
  max_hours_per_request = models.DecimalField(
    max_digits=4,
    decimal_places=2,
    null=True,
    blank=True,
  )
  max_days_per_request = models.IntegerField(null=True, blank=True)
  max_requests_per_year = models.IntegerField(null=True, blank=True)
  requires_documentation = models.BooleanField(default=False)

  def __str__(self):
    return f"Config: {self.type.code}"

  class Meta(BaseModel.Meta):
    db_table = "leave_configuration"
    verbose_name = "Leave Configuration"
    verbose_name_plural = "Leave Configurations"

class TimeoffRequest(BaseModel):
  """
    This contains data about timeoff request

    Fields:
      - type: FK (Type of leave)
      - start_date: DateTime (Start date of the leave request)
      - end_date: DateTime (End date of the leave request)
      - status: Char (Status of the time off request)
      - employee: FK (Employee who is requesting the leave)
      - reason?: Text (Any reason)
  """
  def upload_path(filename):
    file_parts = filename.split(".")
    name = f"{file_parts[0]}-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}.{file_parts[-1]}"

    return os.path.join("timeoff_documents", name)

  type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
  reason = models.TextField(blank=True)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  status = models.CharField(
    max_length=20,
    choices={
      'Requested': 'Requested',
      'Approved': 'Approved',
      'Rejected': 'Rejected',
    },
    default='Requested',
  )
  employee = models.ForeignKey(JobProfile, on_delete=models.PROTECT)
  document = models.FileField(
    upload_to=upload_path,
    blank=True,
    null=True,
    verbose_name="Document Proof",
    validators=[
      FileExtensionValidator(allowed_extensions=["pdf", "jpg", "png", "jpeg"])
    ],
    help_text="Upload a document proof if required (only image or pdf)"
  )

  def __str__(self):
    return f"Time of request by {self.employee.employee.user.username}"

  class Meta(BaseModel.Meta):
    db_table = "timeoff_request"
    verbose_name = "Time off request"
    verbose_name_plural = "Time off requests"

class LeaveBalance(BaseModel):
  """
    This model contains details about leave balance

    Fields:
      - job_profile: FK (connected job profile the balaance)
      - type: FK (connect with Leave Type)
      - balance: Float (actual balance)
  """
  job_profile = models.ForeignKey(JobProfile, on_delete=models.PROTECT)
  type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
  balance = models.FloatField(blank=False)

  def __str__(self):
    return f'{self.job_profile.employee.user.username}:({self.type}-{self.balance})'

  class Meta(BaseModel.Meta):
    db_table = "leave_balance"
    verbose_name = "Leave Balance"
    verbose_name_plural = "Leave Balances"

class LeaveLedger(BaseModel):
  """
    Record / Audit each actions that has happened in the leave balance

    Fields:
      - employee: FK (employee's job profile)
      - leave_type: FK (leave type)
      - amount: Float (amount that is added or deducted)
      - transaction_type: Choice (type of transaction that has happened)
  """
  employee = models.ForeignKey(
    JobProfile,
    on_delete=models.PROTECT,
  )
  leave_type = models.ForeignKey(
    LeaveType,
    on_delete=models.CASCADE,
  )
  amout = models.FloatField(default=0.0)
  transaction_type = models.CharField(max_length=10, choices={
    'accurated': 'accurated',
    'deducted': 'deducted',
    'reset': 'reset',
    'overflow': 'overflow',
    'borrowed': 'borrow'
  })

  def __str__(self):
    return f"Ledger - {self.employee.employee.user.username} | {self.leave_type.code}"

  class Meta(BaseModel.Meta):
    db_table = "leave_ledger"
    verbose_name = "Leave Ledger"
    verbose_name_plural = "Leave Ledgers"
