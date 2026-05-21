from django.test import TestCase

from ..models import Department

class DepartmentTest(TestCase):
  def setUp(self):
    self.dept = Department.objects.create(name="Test Department")

  def test_department_creation(self):
    self.assertEqual(self.dept.name, "Test Department")

  def test_string_representation(self):
    self.assertEqual(str(self.dept), "Test Department")
