from django.test import TestCase

from ..models import Department, Unit

class UnitTest(TestCase):
  def setUp(self):
    self.depart = Department.objects.create(name="Test Department")
    self.unit = Unit.objects.create(name="Test Unit", department=self.depart)

  def test_unit_creation(self):
    self.assertEqual(self.unit.name, "Test Unit")

    self.assertEqual(self.unit.department, self.depart)
    self.assertEqual(self.unit.department.name, "Test Department")

  def test_department_backward_relationship(self):
    all_units_in_deprt = self.depart.unit_set.all()

    self.assertIn(self.unit, all_units_in_deprt)
    self.assertEqual(all_units_in_deprt.count(), 1)

  def test_string_representation(self):
    self.assertEqual(str(self.unit), "Test Unit")
