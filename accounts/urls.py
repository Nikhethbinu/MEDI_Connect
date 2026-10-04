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
    path('administrator/patients/', views.admin_patients, name='admin_patients'),
    path('administrator/doctors/', views.admin_doctors, name='admin_doctors'),
    path('administrator/departments/', views.admin_departments, name='admin_departments'),
    path('administrator/departments/create/', views.admin_department_create, name='admin_department_create'),
    path('administrator/departments/<int:department_id>/edit/', views.admin_department_edit, name='admin_department_edit'),
    path('administrator/departments/<int:department_id>/toggle/', views.admin_department_toggle, name='admin_department_toggle'),
    # ==========================================
    # ADMIN MANAGEMENT
    # ==========================================

    path(
        'administrator/dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'administrator/patients/',
        views.admin_patients,
        name='admin_patients'
    ),

    path(
        'administrator/doctors/',
        views.admin_doctors,
        name='admin_doctors'
    ),

    path(
        'administrator/departments/',
        views.admin_departments,
        name='admin_departments'
    ),

    path(
        'administrator/departments/add/',
        views.admin_department_create,
        name='admin_department_create'
    ),

    path(
        'administrator/departments/<int:department_id>/edit/',
        views.admin_department_edit,
        name='admin_department_edit'
    ),

    path(
        'administrator/departments/<int:department_id>/toggle/',
        views.admin_department_toggle,
        name='admin_department_toggle'
    ),

    path(
        'administrator/appointments/',
        views.admin_appointments,
        name='admin_appointments'
    ),
    path('administrator/prescriptions/', views.admin_prescriptions, name='admin_prescriptions'),
    path('administrator/medical-records/', views.admin_medical_records, name='admin_medical_records'),
    path('administrator/payments/', views.admin_payments, name='admin_payments'),
    path('administrator/reports/', views.admin_reports, name='admin_reports'),
    # ------------------------------------------
    # LOGOUT
    # ------------------------------------------

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
]