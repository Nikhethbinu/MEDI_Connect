from django.contrib import admin

from .models import MedicalRecord


# ==========================================
# MEDICAL RECORD ADMIN
# ==========================================

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'appointment',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'patient__name',
        'patient__username',
        'appointment__appointment_date',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )