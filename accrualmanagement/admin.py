from django.contrib import admin

from .models import Accrual, Tenure, AccrualStrategy

@admin.register(Tenure)
class TenureAdmin(admin.ModelAdmin):
  list_display=("experience", "min_days", "max_days")

@admin.register(AccrualStrategy)
class AccrualStrategyAdmin(admin.ModelAdmin):
  list_display=("leave_type", "type",)

@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
  list_display=("strategy", "tenure", "accrual_rate",)
