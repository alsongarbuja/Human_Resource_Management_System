from django.contrib import admin

from .models import EmployeeType, Role, PayFrequency, EmployeeProfile, JobProfile

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
  list_display=("name",)
  search_fields=("name",)
  order=("name",)

@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
  list_display=("name",)
  search_fields=("name",)
  order=("name",)

@admin.register(PayFrequency)
class PayFrequencyAdmin(admin.ModelAdmin):
  list_display=("name",)
  search_fields=("name",)
  order=("name",)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
  list_display=("user", "unique_id", "address",)
  search_fields=("user", "address",)
  order=("user", "unique_id",)

@admin.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
  list_display=("employee", "unit", "employee_type", "role", "tenure",)
  search_fields=("employee", "unit",)
  order=("employee", "unit", "employee_type", "role", "tenure",)
  list_filter=("unit", "employee_type", "role",)
