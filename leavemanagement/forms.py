from django import forms

from .models import LeaveBalance

class TimeOffRequestForm(forms.Form):
  type = forms.ChoiceField(choices=[])
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
      ).select_related('type')

      self.fields['type'].choices = [
        (lb.type.id, str(lb.type.code)) for lb in available_balances
      ]
