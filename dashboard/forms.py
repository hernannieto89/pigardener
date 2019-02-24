from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import SimpleTimer


class SimpleTimerForm(ModelForm):

    class Meta:
        model = SimpleTimer
        fields = ['start_time', 'end_time', 'work_time', 'sleep_time']

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time not in range(0, 24):
            raise ValidationError('Wrong start_time')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if end_time not in range(0, 24):
            raise ValidationError('Wrong end_time')
        return end_time
