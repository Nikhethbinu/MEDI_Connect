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
        'profile/',views.doctor_profile,name='doctor_profile'
    ),
    # ------------------------------------------
# DOCTOR AVAILABILITY
# ------------------------------------------

path(
    'availability/',views.doctor_availability,name='doctor_availability'
),
#DOCTOR AVAILABILITY DELETE
path(
    'availability/delete/<int:availability_id>/',views.delete_availability,name='delete_availability'
),
#DOCTOR AVAILABILITY EDIT
path(
    'availability/edit/<int:availability_id>/',views.edit_availability,name='edit_availability'
),
#DOCTOR SEARCH
path(
    'search/',views.doctor_search,name='doctor_search'
),
path('detail/<int:doctor_id>/',views.doctor_detail,name='doctor_detail')            

]