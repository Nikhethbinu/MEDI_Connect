from django.db import models

from accounts.models import User
from doctors.models import Doctor


# ==========================================
# APPOINTMENT MODEL
# ==========================================

class Appointment(models.Model):

    # ------------------------------------------
    # APPOINTMENT STATUS
    # ------------------------------------------

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    # ------------------------------------------
    # PATIENT
    # ------------------------------------------

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    # ------------------------------------------
    # DOCTOR
    # ------------------------------------------

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    # ------------------------------------------
    # APPOINTMENT DATE & TIME
    # ------------------------------------------

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    # ------------------------------------------
    # APPOINTMENT REASON
    # ------------------------------------------

    reason = models.TextField(
        blank=True
    )

    # ------------------------------------------
    # STATUS
    # ------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # ------------------------------------------
    # TIMESTAMP
    # ------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
        # ------------------------------------------
    # DATABASE CONSTRAINTS
    # ------------------------------------------

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'doctor',
                    'appointment_date',
                    'appointment_time'
                ],
                name='unique_doctor_appointment_slot'
            )
        ]

    # ------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):

        return (
            f"{self.patient.name} - "
            f"Dr. {self.doctor.user.name} - "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )