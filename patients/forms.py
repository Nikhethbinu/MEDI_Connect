from django import forms
from .models import Patient


# ==========================================
# PATIENT PROFILE FORM
# ==========================================

class PatientProfileForm(forms.ModelForm):

    # ------------------------------------------
    # DATE OF BIRTH FIELD
    # ------------------------------------------

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )


    # ------------------------------------------
    # FORM CONFIGURATION
    # ------------------------------------------

    class Meta:

        model = Patient

        fields = [
            'date_of_birth',
            'gender',
            'address',
            'blood_group',
            'emergency_contact_name',
            'emergency_contact_phone',
        ]