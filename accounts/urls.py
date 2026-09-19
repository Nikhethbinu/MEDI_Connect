from django.urls import path
from . import views


# ==========================================
# ACCOUNT URL PATTERNS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # REGISTRATION
    # ------------------------------------------

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'register/success/',
        views.register_success,
        name='register_success'
    ),


    # ------------------------------------------
    # LOGIN
    # ------------------------------------------

    path(
        'login/',
        views.user_login,
        name='login'
    ),


    # ------------------------------------------
    # MAIN DASHBOARD
    # ------------------------------------------

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    # ------------------------------------------
    # ROLE-BASED DASHBOARDS
    # ------------------------------------------

    path(
        'patient/dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    path(
        'doctor/dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),

    path(
    'administrator/dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
    ),


    # ------------------------------------------
    # LOGOUT
    # ------------------------------------------

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
]