
from django.test import TestCase

from .forms import RegistrationForm
from .models import User


# ==========================================
# REGISTRATION FORM TESTS
# ==========================================

class RegistrationFormTests(TestCase):

    def test_phone_with_letters_is_invalid(self):
        form = RegistrationForm(data={
            'username': 'testuser1',
            'name': 'Test User',
            'phone': '12345abcde',
            'email': 'test1@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_whitespace_only_name_is_invalid(self):
        form = RegistrationForm(data={
            'username': 'testuser2',
            'name': '   ',
            'phone': '9876543210',
            'email': 'test2@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate_email_is_invalid(self):
        User.objects.create_user(
            username='existinguser',
            name='Existing User',
            phone='9876543210',
            email='existing@example.com',
            password='StrongPass123!',
        )

        form = RegistrationForm(data={
            'username': 'newuser',
            'name': 'New User',
            'phone': '9123456780',
            'email': 'EXISTING@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_registration_form(self):
        form = RegistrationForm(data={
            'username': 'validuser',
            'name': 'Valid User',
            'phone': '9123456780',
            'email': 'valid@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid(), form.errors)
