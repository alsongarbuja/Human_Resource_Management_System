from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
  path("dashboard/", views.dashboard, name="dashboard"),
  path("units/", views.select_unit, name="unitSelection"),
  path("select-unit/", views.set_active_unit, name="set_active_unit"),
]
