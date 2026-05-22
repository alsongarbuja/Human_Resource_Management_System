from django import forms

from .models import LeaveBalance

class TimeOffRequestForm(forms.Form):
  leave_type = forms.ChoiceField(choices=[])
  start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
  reason = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Provide brief details...'}))

  def __init__(self, *args, **kwargs):
    jp = kwargs.pop('job_profile', None)

    super(TimeOffRequestForm, self).__init__(*args, **kwargs)

    if jp:
      available_balances = LeaveBalance.objects.filter(
        job_profile=jp,
        balance__gt=0,
      ).select_related('pay_code')

    self.fields['leave_type'].choices = [
      (lb.pay_code.id, str(lb.pay_code)) for lb in available_balances
    ]
