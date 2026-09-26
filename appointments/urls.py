from django.urls import path

from . import views


# ==========================================
# APPOINTMENT URL PATTERNS
# ==========================================

urlpatterns = [

    # ------------------------------------------
    # BOOK APPOINTMENT
    # ------------------------------------------

    path(
        'book/<int:doctor_id>/',views.book_appointment,name='book_appointment'),
    path('success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]