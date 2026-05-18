from django.db import models

from employeemanagement.models import EmployeeProfile, JobProfile

#
# * Punch Entry Model
class PunchEntry(models.Model):
  """
    This contains the punch entry data of employee

    Fields:
      - employee: FK (connected employee profile)
      - job_profile: FK (connected job profile)
      - clock_in: DateTime (Timestamp of clock in)
      - clock_out: DateTime (Timestamp of clock out)
      - ip_address?: IPAddress (Ip address of the clock in/out machine)
  """
  employee = models.ForeignKey(EmployeeProfile, on_delete=models.PROTECT)
  job_profile = models.ForeignKey(JobProfile, on_delete=models.PROTECT)

  clock_in = models.DateTimeField(db_index=True)
  clock_out = models.DateTimeField(null=True, blank=True, db_index=True)

  ip_address = models.GenericIPAddressField(blank=True, null=True)

  def __str__(self):
    status = "Active" if not self.clock_out else f"Ended at {self.clock_out.strftime('%H:%M')}"
    return f"{self.employee} ({self.job_profile.unit}) | {status}"

  class Meta:
    db_table = "punch_entry"
    verbose_name = "Punch Entry"
    verbose_name_plural = "Punch Entries"

    indexes = [
      models.Index(fields=["employee", "-clock_in"])
    ]
