from django.urls import path
from . import views


# ==========================================
# DOCTOR URL PATTERNS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # DOCTOR PROFILE
    # ------------------------------------------

    path(
        'profile/',
        views.doctor_profile,
        name='doctor_profile'
    ),

]