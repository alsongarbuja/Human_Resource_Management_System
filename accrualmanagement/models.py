from django.db import models

from core.models import BaseModel

# * Tenure Model
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

# * Accrual Rate
class Accrual(BaseModel):
  """
    This model contains details related to accrual rate

    Fields:
      - tenure: FK (connected tenure)
      - accrual_rate: float (accrual rate)
  """
  tenure = models.ForeignKey(Tenure, on_delete=models.PROTECT)
  accrual_rate = models.FloatField(default=0.0)

  def __str__(self):
    return f'{self.tenure} - {self.accrual_rate}'

  class Meta(BaseModel.Meta):
    db_table = "accrual_rate"
    verbose_name = "Accrual Rate"
    verbose_name_plural = "Accrual Rates"
