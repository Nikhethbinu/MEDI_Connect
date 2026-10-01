from django.urls import path

from . import views


# ==========================================
# MEDICAL RECORD URLS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # CREATE RECORD
    # ------------------------------------------

    path(
        'create/<int:appointment_id>/',
        views.create_medical_record,
        name='create_medical_record'
    ),

    # ------------------------------------------
    # RECORD DETAIL
    # ------------------------------------------

    path(
        'detail/<int:record_id>/',
        views.medical_record_detail,
        name='medical_record_detail'
    ),

    # ------------------------------------------
    # PATIENT RECORDS
    # ------------------------------------------

    path(
        'patient/',
        views.patient_medical_records,
        name='patient_medical_records'
    ),

]