from django.test import TestCase

from ..models import PayFrequency

class PayFrequencyTest(TestCase):
  def setUp(self):
    self.payFrequency = PayFrequency.objects.create(name="Test PayFrequency")

  def test_payFrequency_creation(self):
    self.assertEqual(self.payFrequency.name, "Test PayFrequency")

  def test_string_rep(self):
    self.assertEqual(str(self.payFrequency), "Test PayFrequency")
