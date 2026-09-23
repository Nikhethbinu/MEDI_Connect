from django.db import models
from accounts.models import User

# ==========================================
# DEPARTMENT MODEL
# ==========================================

class Department(models.Model):

    # ------------------------------------------
    # DEPARTMENT INFORMATION
    # ------------------------------------------

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    # ------------------------------------------
    # STATUS
    # ------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    # ------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):
        return self.name
# ==========================================
# DOCTOR MODEL
# ==========================================

class Doctor(models.Model):

    # ------------------------------------------
    # USER ACCOUNT
    # ------------------------------------------

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )

    # ------------------------------------------
    # PROFESSIONAL INFORMATION
    # ------------------------------------------

    specialization = models.CharField(
        max_length=100
    )

    qualification = models.CharField(
        max_length=150
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    # ------------------------------------------
    # DEPARTMENT
    # ------------------------------------------

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )

    # ------------------------------------------
    # PROFESSIONAL DETAILS
    # ------------------------------------------

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bio = models.TextField(
        blank=True
    )

    # ------------------------------------------
    # STATUS
    # ------------------------------------------

    is_available = models.BooleanField(
        default=True
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
        return f"Dr. {self.user.name} - {self.specialization}"

# ==========================================
# DOCTOR AVAILABILITY MODEL
# ==========================================

class DoctorAvailability(models.Model):

    # ------------------------------------------
    # DAYS OF THE WEEK
    # ------------------------------------------

    DAY_CHOICES = (
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    )

    # ------------------------------------------
    # DOCTOR
    # ------------------------------------------

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )

    # ------------------------------------------
    # AVAILABILITY DAY
    # ------------------------------------------

    day = models.CharField(
        max_length=10,
        choices=DAY_CHOICES
    )

    # ------------------------------------------
    # TIME
    # ------------------------------------------

    start_time = models.TimeField()

    end_time = models.TimeField()

    # ------------------------------------------
    # STATUS
    # ------------------------------------------

    is_active = models.BooleanField(
        default=True
    )
    # ------------------------------------------
    # DATABASE CONSTRAINTS
    # ------------------------------------------

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'doctor',
                    'day',
                    'start_time',
                    'end_time'
                ],
                name='unique_doctor_availability'
            )
        ]
    # ------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------

    def __str__(self):
        return (
            f"{self.doctor.user.name} - "
            f"{self.day} "
            f"{self.start_time} to {self.end_time}"
        )