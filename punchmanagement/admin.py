from django.contrib import admin, messages
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import (
    timezone,
)
from .models import PunchEntry, PayPeriod

@admin.register(PayPeriod)
class PayPeriodAdmin(admin.ModelAdmin):
  list_display=("start_date", "end_date",)
  order=("start_date", "end_date",)

  def get_urls(self):
    """
    Adds the custom 'generate/' URL route to this admin layout.
    """
    urls = super().get_urls()
    custom_urls = [
      path(
        'generate/',
        self.admin_site.admin_view(self.generate_pay_periods_view),
        name='generate_pay_periods',
      ),
    ]
    return custom_urls + urls

  def generate_pay_periods_view(self, request):
    """
    The view that handles the button click logic.
    """
    try:
      created_count, _ = PayPeriod.generate_pay_period_bi_weekly()

      self.message_user(
        request,
        f"Successfully generated {created_count} new pay periods.",
        messages.SUCCESS
      )
    except Exception as e:
      self.message_user(
        request,
        f"An error occurred while generating pay periods: {str(e)}",
        messages.ERROR
      )

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "../"))

@admin.register(PunchEntry)
class PunchEntryAdmin(admin.ModelAdmin):
  list_display=("employee", "clock_in", "clock_out",)
  search_fields=("employee",)
  order=("clock_in", "clock_out",)
