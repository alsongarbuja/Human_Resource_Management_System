from django.contrib import admin

from .models import Kiosk

@admin.register(Kiosk)
class KoiskAdmin(admin.ModelAdmin):
  list_display=("name", "department",)
  search_fields=("name",)
  list_filter=("department",)
