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

]