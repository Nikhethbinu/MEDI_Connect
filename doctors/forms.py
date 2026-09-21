from django import forms
from .models import Doctor


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