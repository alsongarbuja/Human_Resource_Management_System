from django.test import TestCase

from ..models import EmployeeType

class EmployeeTypeTest(TestCase):
  def setUp(self):
    self.employeeType = EmployeeType.objects.create(name="Test Employee Type")

  def test_employeeType_creation(self):
    self.assertEqual(self.employeeType.name, "Test Employee Type")

  def test_string_rep(self):
    self.assertEqual(str(self.employeeType), "Test Employee Type")
