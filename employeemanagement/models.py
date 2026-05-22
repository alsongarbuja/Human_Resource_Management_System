from django.db import models
from datetime import date

from core.models import BaseModel
from organizationmanagement.models import Unit

# * Role Model
class Role(BaseModel):
  """
    This contains the detail about the role in the system

    Fields:
      - name: char (name of the role)
      - description?: Text (optional description field)
  """
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "role"
    verbose_name = "Role"
    verbose_name_plural = "Roles"

# * Empoyee Type Model
class EmployeeType(BaseModel):
  """
    This contains the details about the employee types in the system

    Fields:
      - name: char (name of the employee type)
      - description?: text (description of the type of employee)
  """
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "employee_type"
    verbose_name = "Employee Type"
    verbose_name_plural = "Employee Types"

# * Pay Frequency
class PayFrequency(BaseModel):
  """
    This contains all information on pay frequency

    Fields:
      - name: char (name of the pay frequency)
      - description?: text (description of the type of pay frequency)
  """
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "pay_frequency"
    verbose_name = "Pay Frequency"
    verbose_name_plural = "Pay Frequency"

# * Employee Profile Model
class EmployeeProfile(BaseModel):
  """
    This contains the details that a employee must have in the system

    Fields:
      - user: FK (a one on one relation with user)
      - unique_id: PK (a unique number identifying the user)
      - address?: char (address of the employee)
  """
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

# * Profile Template Model
class ProfileTemplate(BaseModel):
  """
    This contains the details of a profile template that can be reused for job profile

    Fields:
      - role: FK (a one on one relation with role)
      - unit: FK (a one on one relation with unit)
      - employee_type: FK (a one on one relation with employee type)
      - pay_frequency: FK (a one on one relation with pay frequency)
  """
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
  pay_frequency = models.ForeignKey(PayFrequency, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.role} - {self.unit} | {self.employee_type} : {self.pay_frequency}'

  class Meta(BaseModel.Meta):
    db_table = "profile_template"
    verbose_name = "Profile Template"
    verbose_name_plural = "Profle Templates"
    unique_together = ("role", "unit", "employee_type", "pay_frequency",)


# * Job Profile Model
class JobProfile(BaseModel):
  """
    This contains the details that a employee must have in different department

    Fields:
      - employee: FK (a one on one relation with employee profile)
      - tenure: decimal (auto calculated tenure in years of the employee in the current job profile)
      - profile_template: FK (connect with profile template)
      - is_primary: bool (boolean flag to check if this job profile is the primary)
      - hire_date: date (date of hire for this job profile)
      - end_date: date | null (date of end of the job profile)
  """
  employee = models.ForeignKey(EmployeeProfile, on_delete=models.PROTECT)
  profile_template = models.ForeignKey(
    ProfileTemplate,
    on_delete=models.PROTECT,
    related_name="job_profile_template",
  )
  tenure = models.DecimalField(
    max_digits=4, decimal_places=2, default=0.0, null=True, editable=False
  )
  is_primary = models.BooleanField(default=False)
  hire_date = models.DateTimeField(blank=False)
  end_date = models.DateTimeField(blank=True, null=True)

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
