from django.contrib import admin

from .models import EmployeeType, Role, PayFrequency, EmployeeProfile, JobProfile, ProfileTemplate

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

@admin.register(ProfileTemplate)
class ProfileTemplateAdmin(admin.ModelAdmin):
  list_display=("role", "unit", "employee_type", "pay_frequency",)
  search_fields=("role", "unit",)
  list_filter=("pay_frequency", "employee_type", "role", "unit",)


@admin.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
  list_display=("employee", "tenure", "hire_date", "end_date", "is_primary",)
  # search_fields=("employee",)
