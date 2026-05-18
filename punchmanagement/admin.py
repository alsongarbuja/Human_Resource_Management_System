from django.contrib import admin

from .models import PunchEntry

@admin.register(PunchEntry)
class PunchEntryAdmin(admin.ModelAdmin):
  list_display=("employee", "clock_in", "clock_out",)
  search_fields=("employee",)
  order=("clock_in", "clock_out",)
