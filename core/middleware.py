from django.utils.deprecation import MiddlewareMixin
from organizationmanagement.models import Unit
from employeemanagement.models import Role

class ActiveUnitMiddleware(MiddlewareMixin):
  def process_request(self, request):
    """
    Automatically injects the selected Unit model instance into
    the request object if an ID exists in the session store.
    """
    request.active_unit = None

    if request.user.is_authenticated:
      active_unit_id = request.session.get('active_unit_id')
      if active_unit_id:
        try:
          request.active_unit = Unit.objects.get(id=active_unit_id)
        except Unit.DoesNotExist:
          del request.session['active_unit_id']

class ActiveProfileRoleMiddleware(MiddlewareMixin):
  def process_request(self, request):
    """
    Automatically inject the role of the currently selected
    job profile to the request object.
    """
    request.role = None

    if request.user.is_authenticated:
      active_role_id = request.session.get('active_role_id')
      if active_role_id:
        try:
          request.role = Role.objects.get(id=active_role_id)
        except Role.DoesNotExist:
          del request.session['role']
