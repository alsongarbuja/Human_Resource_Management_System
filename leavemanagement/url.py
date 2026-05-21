from django.urls import path

from . import views

app_name = "leave"

urlpatterns = [
  path("time-off-requests/", views.timeOffRequests, name="timeoffRequests"),
]
