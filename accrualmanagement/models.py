from django.db import models

from core.models import BaseModel
from leavemanagement.models import LeaveType

class Tenure(BaseModel):
  """
    This model contains details related to tenure

    Fields:
      - experience: Char (experience of the employee)
      - min_days: int (minimum number of days being employeed for this experience to apply)
      - max_days!: int (maximum number of days being employeed for this experience to apply)
  """
  experience = models.CharField(max_length=50, unique=True)
  min_days = models.BigIntegerField(default=0)
  max_days = models.BigIntegerField(null=True)

  def __str__(self):
    return self.experience

  class Meta(BaseModel.Meta):
    db_table = "tenure"
    verbose_name = "Tenure"
    verbose_name_plural = "Tenures"

class AccrualStrategy(BaseModel):
  """
    Different strategy of accrual

    Fields:
      - leave_type: FK (type of leave)
      - type: Enum (type of accrual strategy)
  """
  leave_type = models.ForeignKey(
    LeaveType,
    on_delete=models.SET_NULL,
    null=True,
  )
  type = models.CharField(max_length=20, choices={
    'fixed': 'fixed',
    'variable': 'variable',
  })

  def __str__(self):
    return f"Strategy ({self.leave_type})"

  class Meta(BaseModel.Meta):
    db_table = "accrual_strategy"
    verbose_name = "Accrual Strategy"
    verbose_name_plural = "Accrual Strategies"

class Accrual(BaseModel):
  """
    This model contains details related to accrual rate

    Fields:
      - strategy: FK (connected strategy)
      - tenure?: FK (connected tenure)
      - accrual_rate: float (accrual rate)
  """
  strategy = models.ForeignKey(AccrualStrategy, on_delete=models.SET_NULL, null=True)
  tenure = models.ForeignKey(Tenure, on_delete=models.SET_NULL, null=True, blank=True)
  accrual_rate = models.FloatField(default=0.0)

  def __str__(self):
    return f'{self.tenure} - {self.accrual_rate}'

  class Meta(BaseModel.Meta):
    db_table = "accrual_rate"
    verbose_name = "Accrual Rate"
    verbose_name_plural = "Accrual Rates"
