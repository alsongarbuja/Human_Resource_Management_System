from django.test import TestCase

from ..models import Role

class RoleTest(TestCase):
  def setUp(self):
    self.role = Role.objects.create(name="Test Role")

  def test_role_creation(self):
    self.assertEqual(self.role.name, "Test Role")

  def test_string_rep(self):
    self.assertEqual(str(self.role), "Test Role")
