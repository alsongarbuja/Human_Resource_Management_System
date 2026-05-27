from django.contrib import admin

from .models import LeaveType, LeaveConfiguration, TimeoffRequest, LeaveBalance

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
  list_display=("name", "code",)
  search_fields=("name", "code",)

@admin.register(LeaveConfiguration)
class LeaveConfigurationAdmin(admin.ModelAdmin):
  list_display=("type", "initial_balance", "requires_documentation",)

@admin.register(TimeoffRequest)
class TimeoffRequestAdmin(admin.ModelAdmin):
  pass

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
  list_display=("job_profile", "type", "balance",)
  search_fields=("job_profile", "type")
  list_filter=("type",)
