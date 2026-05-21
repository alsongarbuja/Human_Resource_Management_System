from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
  site_header = "Time Clock System Admin"
  site_title = "Time Clock System | Admin Portal"
  index_title = "Welcome to Time Clock System"

  def get_app_list(self, request):
    return super().get_app_list(request)

custom_admin_site = CustomAdminSite(name="admin_portal")
