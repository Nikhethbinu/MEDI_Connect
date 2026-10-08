from django.urls import path
from . import views


# ==========================================
# PATIENT URL PATTERNS
# ==========================================

urlpatterns = [

    path(
        'profile/',
        views.patient_profile,
        name='patient_profile'
    ),
    path(
        'profile/edit/',
        views.edit_patient_profile,
        name='edit_patient_profile'
    ),

]