from django.db import models

from core.models import BaseModel

#
# * Department Model
class Department(BaseModel):
  """
    This model contains details about the department in the system

    Fields:
      - name: char (name of the department)
      - description?: text (description about the department)
  """
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "department"
    verbose_name = "Department"
    verbose_name_plural = "Departments"

#
# * Unit Model
class Unit(BaseModel):
  """
    This model contains details about a unit in a department

    Fields:
      - name: char (name of the unit)
      - index?: char (unique index number)
      - description?: text (description of the unit)
      - department: FK (connecting unit to the department)
  """
  name = models.CharField(max_length=50, unique=True)
  index = models.CharField(max_length=6, blank=True)
  description = models.TextField(blank=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "unit"
    verbose_name = "Unit"
    verbose_name_plural = "Units"
