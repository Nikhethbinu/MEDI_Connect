
from django import forms
from django.utils import timezone

from .models import Doctor, DoctorAvailability, Department


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

        widgets = {
            'specialization': forms.TextInput(
                attrs={
                    'placeholder': 'Example: Cardiologist'
                }
            ),

            'qualification': forms.TextInput(
                attrs={
                    'placeholder': 'Example: MBBS, MD Cardiology'
                }
            ),

            'experience_years': forms.NumberInput(
                attrs={
                    'min': 0,
                    'placeholder': 'Years of experience'
                }
            ),

            'department': forms.Select(),

            'consultation_fee': forms.NumberInput(
                attrs={
                    'min': 0,
                    'step': '0.01',
                    'placeholder': 'Consultation fee'
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Write a short professional biography...'
                }
            ),

            'is_available': forms.CheckboxInput(),
        }

    # ------------------------------------------
    # SPECIALIZATION VALIDATION
    # ------------------------------------------

    def clean_specialization(self):
        specialization = self.cleaned_data['specialization'].strip()

        if not specialization:
            raise forms.ValidationError(
                'Specialization cannot be empty.'
            )

        return specialization

    # ------------------------------------------
    # QUALIFICATION VALIDATION
    # ------------------------------------------

    def clean_qualification(self):
        qualification = self.cleaned_data['qualification'].strip()

        if not qualification:
            raise forms.ValidationError(
                'Qualification cannot be empty.'
            )

        return qualification

    # ------------------------------------------
    # EXPERIENCE VALIDATION
    # ------------------------------------------

    def clean_experience_years(self):
        experience_years = self.cleaned_data['experience_years']

        if experience_years < 0:
            raise forms.ValidationError(
                'Experience years cannot be negative.'
            )

        return experience_years

    # ------------------------------------------
    # CONSULTATION FEE VALIDATION
    # ------------------------------------------

    def clean_consultation_fee(self):
        consultation_fee = self.cleaned_data['consultation_fee']

        if consultation_fee < 0:
            raise forms.ValidationError(
                'Consultation fee cannot be negative.'
            )

        return consultation_fee

    # ------------------------------------------
    # BIO VALIDATION
    # ------------------------------------------

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '')

        if bio and not bio.strip():
            raise forms.ValidationError(
                'Biography cannot contain only blank spaces.'
            )

        return bio.strip()


# ==========================================
# DOCTOR AVAILABILITY FORM
# ==========================================

class DoctorAvailabilityForm(forms.ModelForm):

    class Meta:
        model = DoctorAvailability

        fields = [
            'availability_date',
            'start_time',
            'end_time',
        ]

        widgets = {
            'availability_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'mc-input',
                }
            ),

            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'mc-input',
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'mc-input',
                }
            ),
        }

    # ------------------------------------------
    # AVAILABILITY DATE VALIDATION
    # ------------------------------------------

    def clean_availability_date(self):
        availability_date = self.cleaned_data['availability_date']

        if availability_date < timezone.localdate():
            raise forms.ValidationError(
                'Availability date cannot be in the past.'
            )

        return availability_date

    # ------------------------------------------
    # AVAILABILITY TIME VALIDATION
    # ------------------------------------------

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        availability_date = cleaned_data.get('availability_date')

        if start_time and end_time and start_time >= end_time:
            self.add_error(
                'end_time',
                'End time must be later than start time.'
            )

        if (
            availability_date == timezone.localdate()
            and start_time
            and end_time
        ):
            current_time = timezone.localtime().time()

            if end_time <= current_time:
                self.add_error(
                    'end_time',
                    'Availability must end in the future.'
                )

        return cleaned_data


# ==========================================
# DEPARTMENT FORM
# ==========================================

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department

        fields = [
            'name',
            'description',
            'is_active',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter department name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter department description'
                }
            ),

            'is_active': forms.CheckboxInput(),
        }

    # ------------------------------------------
    # DEPARTMENT NAME VALIDATION
    # ------------------------------------------

    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if not name:
            raise forms.ValidationError(
                'Department name cannot be empty.'
            )

        return name
