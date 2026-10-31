
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from django.contrib.auth.password_validation import validate_password
from doctors.models import Department

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

class AdminDoctorCreationForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        label="Doctor Name"
    )

    username = forms.CharField(
        max_length=150,
        label="Username (Login ID)"
    )

    phone = forms.CharField(
        max_length=15,
        label="Phone Number"
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    specialization = forms.CharField(
        max_length=100
    )

    qualification = forms.CharField(
        max_length=150
    )

    experience_years = forms.IntegerField(
        min_value=0
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True)
    )

    consultation_fee = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        from accounts.models import User

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "This username is already registered."
            )

        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()

        from accounts.models import User

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Enter a valid 10-digit phone number."
            )

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "This phone number is already registered."
            )

        return phone

    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if not name:
            raise forms.ValidationError(
                "Doctor name cannot be empty."
            )

        return name

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    "Passwords do not match."
                )
            else:
                try:
                    validate_password(password1)
                except forms.ValidationError as error:
                    self.add_error('password1', error)

        return cleaned_data