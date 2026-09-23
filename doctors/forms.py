from django import forms
from .models import Doctor,DoctorAvailability


# ==========================================
# DOCTOR PROFILE FORM
# ==========================================

class DoctorProfileForm(forms.ModelForm):

    class Meta:

        model = Doctor

        fields = [
            'specialization',
            'qualification',
            'experience_years',
            'department',
            'consultation_fee',
            'bio',
            'is_available',
        ]

# ==========================================
# DOCTOR AVAILABILITY FORM
# ==========================================

class DoctorAvailabilityForm(forms.ModelForm):

    # ------------------------------------------
    # FORM CONFIGURATION
    # ------------------------------------------

    class Meta:
        model = DoctorAvailability

        fields = [
            'day',
            'start_time',
            'end_time',
        ]

        widgets = {
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),
        }

    # ------------------------------------------
    # TIME VALIDATION
    # ------------------------------------------

    def clean(self):

        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:

            if start_time >= end_time:
                raise forms.ValidationError(
                    'End time must be later than start time.'
                )

        return cleaned_data