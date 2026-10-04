from django.db import models

from accounts.models import User
from appointments.models import Appointment


# ==========================================
# PAYMENT
# ==========================================

class Payment(models.Model):

    # ==========================================
    # PAYMENT STATUS
    # ==========================================

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    # ==========================================
    # PAYMENT METHOD
    # ==========================================

    METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
        ('NET_BANKING', 'Net Banking'),
    )

    # ==========================================
    # APPOINTMENT
    # ==========================================

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # ==========================================
    # PATIENT
    # ==========================================

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    # ==========================================
    # AMOUNT DETAILS
    # ==========================================

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    additional_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # ==========================================
    # PAYMENT DETAILS
    # ==========================================

    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    # ==========================================
    # TIMESTAMPS
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ==========================================
    # STRING REPRESENTATION
    # ==========================================

    def __str__(self):

        return (
            f"Payment - "
            f"{self.patient.name} - "
            f"₹{self.total_amount}"
        )   