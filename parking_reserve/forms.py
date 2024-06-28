import datetime
from django.forms import ModelForm, DateInput, TextInput, ValidationError
from .models import Reservation
from django.contrib import messages

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ['ticket_code', 'customer', 'checked_out']
        # Validating form fields using widgets
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'finish_date': DateInput(attrs={'type': 'date'}),
            'plate_number': TextInput(),
            'phone_number': TextInput(attrs={'pattern': '[0-9]+', 'title': 'Enter digits only '}),
        }

# Additional custom validator for start_date / finish_date fields
    def clean(self):
        data = self.cleaned_data
        start_date = data['start_date']
        finish_date = data['finish_date']

        if start_date > finish_date:
            raise ValidationError('Wrong start and finish dates.')

        if start_date < datetime.date.today():
            raise ValidationError('Start date in the past.')

        return data
