from django.contrib import admin

from .models import Department, Unit

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  list_display=("name",)
  search_fields=("name",)
  order=("name",)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
  list_display=("name", "department",)
  search_fields=("name",)
  order=("name", "department",)
  list_filter=("department",)
