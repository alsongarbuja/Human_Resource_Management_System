from django.contrib import admin

from .models import PayCode, TimeoffRequest, LeaveBalance

@admin.register(PayCode)
class PayCodeAdmin(admin.ModelAdmin):
  list_display=("name", "description",)
  search_fields=("name", "description")

@admin.register(TimeoffRequest)
class TimeoffRequestAdmin(admin.ModelAdmin):
  pass

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
  list_display=("job_profile", "pay_code", "balance",)
  search_fields=("job_profile", "pay_code")
  list_filter=("pay_code",)
