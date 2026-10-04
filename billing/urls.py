from django.urls import path

from . import views


# ==========================================
# BILLING URLS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # CREATE PAYMENT
    # ------------------------------------------

    path(
        'create/<int:appointment_id>/',
        views.create_payment,
        name='create_payment'
    ),

    # ------------------------------------------
    # PAYMENT DETAIL
    # ------------------------------------------

    path(
        'detail/<int:payment_id>/',
        views.payment_detail,
        name='payment_detail'
    ),

    # ------------------------------------------
    # PATIENT PAYMENTS
    # ------------------------------------------

    path(
        'patient/',
        views.patient_payments,
        name='patient_payments'
    ),

]