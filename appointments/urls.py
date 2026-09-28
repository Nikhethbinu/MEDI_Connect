from django.urls import path

from . import views


# ==========================================
# APPOINTMENT URL PATTERNS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # BOOK APPOINTMENT
    # ------------------------------------------

    path('book/<int:doctor_id>/',views.book_appointment,name='book_appointment'),
    path('success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    path('doctor/',views.doctor_appointments,name='doctor_appointments'),
    path('doctor/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('doctor/reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('doctor/complete/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),

]