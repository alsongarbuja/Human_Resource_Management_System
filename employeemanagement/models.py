from django.db import models
from datetime import date

from core.models import BaseModel
from organizationmanagement.models import Unit

class Role(BaseModel):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "role"
    verbose_name = "Role"
    verbose_name_plural = "Roles"

class EmployeeType(BaseModel):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "employee_type"
    verbose_name = "Employee Type"
    verbose_name_plural = "Employee Types"

class PayFrequency(BaseModel):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "pay_frequency"
    verbose_name = "Pay Frequency"
    verbose_name_plural = "Pay Frequency"

class EmployeeProfile(BaseModel):
  user = models.OneToOneField(
    "auth.User", on_delete=models.CASCADE
  )
  address = models.CharField(max_length=200, blank=True)
  unique_id = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.user.username

  class Meta(BaseModel.Meta):
    db_table = "employee_profile"
    verbose_name = "Employee Profile"
    verbose_name_plural = "Employee Profiles"

class JobProfile(BaseModel):
  employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
  pay_frequency = models.ForeignKey(PayFrequency, on_delete=models.CASCADE)
  tenure = models.DecimalField(
    max_digits=4, decimal_places=2, default=0.0, null=True, editable=False
  )

  def __str__(self):
    return self.employee.user.username

  def calculate_tenure(self):
    """Return tenure in years (decimal)."""
    if not getattr(self.employee.user, "date_joined", None):
      return 0.0
    today = date.today()
    join = self.employee.user.date_joined.date()
    days = (today - join).days
    return round(days / 365.25, 2)

  def save(self, *args, **kwargs):
    new_tenure = self.calculate_tenure()
    if self.tenure != new_tenure:
      self.tenure = new_tenure
    super().save(*args, **kwargs)

  class Meta(BaseModel.Meta):
    db_table = "job_profile"
    verbose_name = "Job Profile"
    verbose_name_plural = "Job Profles"
