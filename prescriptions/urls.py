from django.urls import path

from . import views


# ==========================================
# PRESCRIPTION URL PATTERNS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # CREATE PRESCRIPTION
    # ------------------------------------------

    path(
        'create/<int:appointment_id>/',
        views.create_prescription,
        name='create_prescription'
    ),

    # ------------------------------------------
    # PRESCRIPTION DETAIL
    # ------------------------------------------

    path(
        'detail/<int:prescription_id>/',
        views.prescription_detail,
        name='prescription_detail'
    ),
]