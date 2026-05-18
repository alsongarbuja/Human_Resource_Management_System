from django.db import models

from core.models import BaseModel

class Department(BaseModel):
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "department"
    verbose_name = "Department"
    verbose_name_plural = "Departments"

class Unit(BaseModel):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  class Meta(BaseModel.Meta):
    db_table = "unit"
    verbose_name = "Unit"
    verbose_name_plural = "Units"
