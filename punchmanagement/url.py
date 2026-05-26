from django.urls import path

from . import views

app_name = "punch"

urlpatterns = [
  path("clock-in-out/", views.clockInOut, name="clockInOut"),
  path("scan-clock-in-out/", views.scanClockInOut, name="scanClockInOut"),
]
