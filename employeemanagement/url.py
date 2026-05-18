from django.urls import path

from . import views

app_name = "employee_management"

urlpatterns = [
  path("login/", views.login, name="login")
]
