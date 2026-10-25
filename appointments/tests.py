
from datetime import date, time, timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import AppointmentForm


# ==========================================
# APPOINTMENT FORM TESTS
# ==========================================

class AppointmentFormTests(TestCase):

    # ------------------------------------------
    # TEST PAST APPOINTMENT DATE
    # ------------------------------------------

    def test_past_appointment_date_is_invalid(self):
        past_date = timezone.localdate() - timedelta(days=1)

        form = AppointmentForm(data={
            'appointment_date': past_date.isoformat(),
            'appointment_time': '10:00',
            'reason': 'General consultation',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('appointment_date', form.errors)

    # ------------------------------------------
    # TEST VALID FUTURE APPOINTMENT DATE
    # ------------------------------------------

    def test_future_appointment_date_is_valid(self):
        future_date = timezone.localdate() + timedelta(days=1)

        form = AppointmentForm(data={
            'appointment_date': future_date.isoformat(),
            'appointment_time': '10:00',
            'reason': 'General consultation',
        })

        self.assertTrue(form.is_valid(), form.errors)

    # ------------------------------------------
    # TEST WHITESPACE-ONLY REASON
    # ------------------------------------------

    def test_whitespace_only_reason_is_invalid(self):
        future_date = timezone.localdate() + timedelta(days=1)

        form = AppointmentForm(data={
            'appointment_date': future_date.isoformat(),
            'appointment_time': '10:00',
            'reason': '   ',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('reason', form.errors)
