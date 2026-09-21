from django.db import models
from accounts.models import User


# ==========================================
# PATIENT MODEL
# ==========================================

class Patient(models.Model):

    # ------------------------------------------
    # USER ACCOUNT
    # ------------------------------------------

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )

    # ------------------------------------------
    # PERSONAL INFORMATION
    # ------------------------------------------

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    # ------------------------------------------
    # EMERGENCY CONTACT
    # ------------------------------------------

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=15,
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
        return self.user.name