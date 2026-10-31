
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import PatientProfileForm


# ==========================================
# PATIENT PROFILE FORM TESTS
# ==========================================

class PatientProfileFormTests(TestCase):

    def test_future_date_of_birth_is_invalid(self):
        future_date = timezone.localdate() + timedelta(days=1)

        form = PatientProfileForm(data={
            'date_of_birth': future_date.isoformat(),
            'gender': 'Male',
            'address': 'Kottayam',
            'blood_group': 'O+',
            'emergency_contact_name': 'Test Contact',
            'emergency_contact_phone': '9876543210',
        })

        self.assertFalse(
            form.is_valid(),
            f"Future date of birth was accepted. Errors: {form.errors}"
        )
        self.assertIn('date_of_birth', form.errors)

    def test_invalid_emergency_phone_is_rejected(self):
        form = PatientProfileForm(data={
            'date_of_birth': '2000-01-15',
            'gender': 'Male',
            'address': 'Kottayam',
            'blood_group': 'O+',
            'emergency_contact_name': 'Test Contact',
            'emergency_contact_phone': '12345abcde',
        })

        self.assertFalse(
            form.is_valid(),
            f"Invalid emergency phone was accepted. Errors: {form.errors}"
        )
        self.assertIn('emergency_contact_phone', form.errors)

    def test_whitespace_only_address_is_invalid(self):
        form = PatientProfileForm(data={
            'date_of_birth': '2000-01-15',
            'gender': 'Male',
            'address': '   ',
            'blood_group': 'O+',
            'emergency_contact_name': 'Test Contact',
            'emergency_contact_phone': '9876543210',
        })

        self.assertFalse(
            form.is_valid(),
            f"Whitespace-only address was accepted. Errors: {form.errors}"
        )
        self.assertIn('address', form.errors)

    def test_valid_patient_profile(self):
        form = PatientProfileForm(data={
            'date_of_birth': '2000-01-15',
            'gender': 'Male',
            'address': 'Kottayam',
            'blood_group': 'O+',
            'emergency_contact_name': 'Test Contact',
            'emergency_contact_phone': '9876543210',
        })

        self.assertTrue(
            form.is_valid(),
            f"Valid patient profile was rejected. Errors: {form.errors}"
        )
