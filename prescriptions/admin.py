from django.contrib import admin

from .models import (
    Medicine,
    Prescription,
    PrescriptionItem
)


# ==========================================
# MEDICINE ADMIN
# ==========================================

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'dosage_form',
        'is_active',
    ]

    search_fields = [
        'name',
    ]


# ==========================================
# PRESCRIPTION ITEM INLINE
# ==========================================

class PrescriptionItemInline(
    admin.TabularInline
):

    model = PrescriptionItem
    extra = 1


# ==========================================
# PRESCRIPTION ADMIN
# ==========================================

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'appointment',
        'diagnosis',
        'created_at',
    ]

    inlines = [
        PrescriptionItemInline
    ]