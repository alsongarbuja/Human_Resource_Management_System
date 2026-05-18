from django.test import TestCase

from django.contrib.auth.models import User
from ..models import EmployeeProfile

class EmployeeProfileTest(TestCase):
  def setUp(self):
    self.user = User.objects.create(username="test", password="tesT@12345")
    self.empEmployeeProfile = EmployeeProfile.objects.create(user=self.user, unique_id="S09999999")

  def test_empEmployeeProfile_creation(self):
    self.assertEqual(self.empEmployeeProfile.user.username, "test")

  def test_string_rep(self):
    self.assertEqual(str(self.empEmployeeProfile), "test")
