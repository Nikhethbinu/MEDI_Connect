
from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Appointment


# ==========================================
# APPOINTMENT BOOKING FORM
# ==========================================

class AppointmentForm(forms.ModelForm):

    # ------------------------------------------
    # FORM CONFIGURATION
    # ------------------------------------------
    
    reason = forms.CharField(
        required=False,
        strip=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Reason for appointment'
            }
        )
    )

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
        appointment_date = self.cleaned_data['appointment_date']
        today = timezone.localdate()

        if appointment_date < today:
            raise forms.ValidationError(
                'Appointment date cannot be in the past.'
            )

        return appointment_date

    # ------------------------------------------
    # TIME VALIDATION
    # ------------------------------------------

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data['appointment_time']
        appointment_date = self.cleaned_data.get('appointment_date')

        if appointment_date and appointment_time:
            now = timezone.localtime()

            if appointment_date == now.date():
                appointment_datetime = datetime.combine(
                    appointment_date,
                    appointment_time
                )

                current_datetime = datetime.combine(
                    now.date(),
                    now.time().replace(tzinfo=None)
                )

                if appointment_datetime <= current_datetime:
                    raise forms.ValidationError(
                        'Appointment time must be in the future.'
                    )

        return appointment_time

    # ------------------------------------------
    # REASON VALIDATION
    # ------------------------------------------

    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '')

        if reason and not reason.strip():
            raise forms.ValidationError(
                'Reason cannot contain only blank spaces.'
            )

        return reason.strip()
