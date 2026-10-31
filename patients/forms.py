
from django import forms
from django.utils import timezone

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
            attrs={'type': 'date'}
        )
    )

    # Preserve whitespace so clean_address can validate it.
    address = forms.CharField(
        required=False,
        strip=False
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

    # ------------------------------------------
    # DATE OF BIRTH VALIDATION
    # ------------------------------------------

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']

        if date_of_birth > timezone.localdate():
            raise forms.ValidationError(
                'Date of birth cannot be in the future.'
            )

        return date_of_birth

    # ------------------------------------------
    # ADDRESS VALIDATION
    # ------------------------------------------

    def clean_address(self):
        address = self.cleaned_data.get('address', '')

        if address and not address.strip():
            raise forms.ValidationError(
                'Address cannot contain only blank spaces.'
            )

        return address.strip()

    # ------------------------------------------
    # EMERGENCY CONTACT NAME VALIDATION
    # ------------------------------------------

    def clean_emergency_contact_name(self):
        name = self.cleaned_data.get(
            'emergency_contact_name', ''
        )

        if name and not name.strip():
            raise forms.ValidationError(
                'Emergency contact name cannot contain only spaces.'
            )

        return name.strip()

    # ------------------------------------------
    # EMERGENCY CONTACT PHONE VALIDATION
    # ------------------------------------------

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data.get(
            'emergency_contact_phone', ''
        )

        if not phone:
            return phone

        if not phone.isdigit():
            raise forms.ValidationError(
                'Emergency contact phone must contain only digits.'
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                'Emergency contact phone must contain exactly 10 digits.'
            )

        return phone
