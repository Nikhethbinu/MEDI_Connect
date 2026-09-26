from django import forms

from .models import Appointment


# ==========================================
# APPOINTMENT BOOKING FORM
# ==========================================

class AppointmentForm(forms.ModelForm):

    # ------------------------------------------
    # FORM CONFIGURATION
    # ------------------------------------------

    class Meta:

        model = Appointment

        fields = [
            'appointment_date',
            'appointment_time',
            'reason',
        ]

        widgets = {

            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Reason for appointment'
                }
            ),
        }

    # ------------------------------------------
    # DATE VALIDATION
    # ------------------------------------------

    def clean_appointment_date(self):

        appointment_date = (
            self.cleaned_data['appointment_date']
        )

        from datetime import date

        if appointment_date < date.today():

            raise forms.ValidationError(
                'Appointment date cannot be in the past.'
            )

        return appointment_date