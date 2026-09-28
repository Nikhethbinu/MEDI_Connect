from django.db import models


# ==========================================
# MEDICINE MODEL
# ==========================================

class Medicine(models.Model):

    # ------------------------------------------
    # MEDICINE INFORMATION
    # ------------------------------------------

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    dosage_form = models.CharField(
        max_length=50,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
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
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):
        return self.name

# ==========================================
# PRESCRIPTION MODEL
# ==========================================

class Prescription(models.Model):

    # ------------------------------------------
    # APPOINTMENT
    # ------------------------------------------

    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='prescription'
    )

    # ------------------------------------------
    # DOCTOR NOTES
    # ------------------------------------------

    diagnosis = models.TextField(
        blank=True
    )

    notes = models.TextField(
        blank=True
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
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):
        return (
            f"Prescription - "
            f"{self.appointment.patient.name}"
        )

# ==========================================
# PRESCRIPTION ITEM MODEL
# ==========================================

class PrescriptionItem(models.Model):

    # ------------------------------------------
    # PRESCRIPTION
    # ------------------------------------------

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # ------------------------------------------
    # MEDICINE
    # ------------------------------------------

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='prescription_items'
    )

    # ------------------------------------------
    # MEDICATION DETAILS
    # ------------------------------------------

    dosage = models.CharField(
        max_length=100
    )

    frequency = models.CharField(
        max_length=100
    )

    duration = models.CharField(
        max_length=100
    )

    instructions = models.TextField(
        blank=True
    )

    # ------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):
        return (
            f"{self.medicine.name} - "
            f"{self.dosage}"
        )