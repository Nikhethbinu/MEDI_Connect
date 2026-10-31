
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


# ==========================================
# REGISTRATION FORM
# ==========================================

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'name',
            'phone',
            'email',
            'password1',
            'password2',
        ]

    # ------------------------------------------
    # NAME VALIDATION
    # ------------------------------------------

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        if not name.strip():
            raise forms.ValidationError(
                'Name cannot be empty or contain only spaces.'
            )

        return name.strip()

    # ------------------------------------------
    # PHONE VALIDATION
    # ------------------------------------------

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')

        if not phone:
            return phone

        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                'Phone number must contain exactly 10 digits.'
            )

        return phone

    # ------------------------------------------
    # EMAIL VALIDATION
    # ------------------------------------------

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if email and User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                'An account with this email address already exists.'
            )

        return email
