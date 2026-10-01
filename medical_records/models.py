from django.db import models

from accounts.models import User
from appointments.models import Appointment


# ==========================================
# MEDICAL RECORD
# ==========================================

class MedicalRecord(models.Model):

    # ------------------------------------------
    # PATIENT
    # ------------------------------------------

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )

    # ------------------------------------------
    # APPOINTMENT
    # ------------------------------------------

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='medical_record'
    )

    # ------------------------------------------
    # MEDICAL INFORMATION
    # ------------------------------------------

    symptoms = models.TextField(
        blank=True
    )

    diagnosis = models.TextField(
        blank=True
    )

    treatment = models.TextField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    # ------------------------------------------
    # TIMESTAMPS
    # ------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):

        return (
            f"Medical Record - "
            f"{self.patient.name} - "
            f"{self.appointment.appointment_date}"
        )