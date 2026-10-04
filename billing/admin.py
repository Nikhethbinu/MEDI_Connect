from django.contrib import admin

from .models import Payment


# ==========================================
# PAYMENT ADMIN
# ==========================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'appointment',
        'consultation_fee',
        'additional_charges',
        'total_amount',
        'payment_method',
        'status',
        'payment_date',
    )

    search_fields = (
        'patient__name',
        'patient__username',
        'transaction_id',
    )

    list_filter = (
        'status',
        'payment_method',
        'payment_date',
    )