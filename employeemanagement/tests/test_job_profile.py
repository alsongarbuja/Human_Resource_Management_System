from django.test import TestCase

from django.contrib.auth.models import User
from organizationmanagement.models import Unit, Department
from ..models import Role, EmployeeType, PayFrequency, EmployeeProfile, JobProfile

class JobProfileTest(TestCase):
  def setUp(self):
    self.department = Department.objects.create(name="T Department")
    self.unit = Unit.objects.create(name="T unit", department=self.department)

    self.user = User.objects.create(username="test", password="tesT@12345")

    self.employeeProfile = EmployeeProfile.objects.create(user=self.user, unique_id="S09999999")
    self.role = Role.objects.create(name="T Role")
    self.payFrequency = PayFrequency.objects.create(name="T Pay Frequency")
    self.employeeType = EmployeeType.objects.create(name="T Employee Type")
    self.jobProfile = JobProfile.objects.create(
      employee=self.employeeProfile,
      employee_type=self.employeeType,
      role=self.role,
      pay_frequency=self.payFrequency,
      unit=self.unit,
    )

  def test_jobProfile_creation(self):
    self.assertEqual(self.jobProfile.employee.user.username, "test")

    self.assertEqual(self.jobProfile.role.name, self.role.name)
    self.assertEqual(self.jobProfile.employee_type.name, self.employeeType.name)
    self.assertEqual(self.jobProfile.pay_frequency.name, self.payFrequency.name)
    self.assertHasAttr(self.jobProfile, "tenure")

  def test_string_rep(self):
    self.assertEqual(str(self.jobProfile), "test")
