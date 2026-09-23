from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import role_required

from .forms import (
    DoctorProfileForm,
    DoctorAvailabilityForm
)

from .models import (
    Doctor,
    DoctorAvailability,
    Department
)
# ==========================================
# DOCTOR PROFILE
# ==========================================

@login_required
def doctor_profile(request):

    # ------------------------------------------
    # GET EXISTING DOCTOR PROFILE
    # ------------------------------------------

    try:
        doctor = request.user.doctor_profile

    except Doctor.DoesNotExist:
        doctor = None


    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = DoctorProfileForm(
            request.POST,
            instance=doctor
        )

        if form.is_valid():

            # ------------------------------------------
            # SAVE DOCTOR PROFILE
            # ------------------------------------------

            doctor = form.save(commit=False)

            doctor.user = request.user

            doctor.save()

            return redirect('doctor_profile')


    # ------------------------------------------
    # DISPLAY PROFILE FORM
    # ------------------------------------------

    else:

        form = DoctorProfileForm(
            instance=doctor
        )


    # ------------------------------------------
    # RENDER PROFILE PAGE
    # ------------------------------------------

    return render(
        request,
        'doctors/profile.html',
        {'form': form}
    )

# ==========================================
# DOCTOR AVAILABILITY
# ==========================================

@login_required
@role_required('DOCTOR')
def doctor_availability(request):

    # ------------------------------------------
    # GET DOCTOR PROFILE
    # ------------------------------------------

    doctor = request.user.doctor_profile

    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = DoctorAvailabilityForm(
            request.POST
        )

        if form.is_valid():

            # ------------------------------------------
            # SAVE AVAILABILITY
            # ------------------------------------------

            availability = form.save(
                commit=False
            )

            availability.doctor = doctor

            availability.save()

            return redirect(
                'doctor_availability'
            )

    # ------------------------------------------
    # DISPLAY FORM
    # ------------------------------------------

    else:

        form = DoctorAvailabilityForm()

    # ------------------------------------------
    # GET EXISTING AVAILABILITY
    # ------------------------------------------

    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        is_active=True
    ).order_by(
        'day',
        'start_time'
    )

    # ------------------------------------------
    # RENDER PAGE
    # ------------------------------------------

    return render(
        request,
        'doctors/availability.html',
        {
            'form': form,
            'availabilities': availabilities
        }
    )
# ==========================================
# DELETE DOCTOR AVAILABILITY
# ==========================================

@login_required
@role_required('DOCTOR')
def delete_availability(request, availability_id):

    # ------------------------------------------
    # GET DOCTOR PROFILE
    # ------------------------------------------

    doctor = request.user.doctor_profile

    # ------------------------------------------
    # GET AVAILABILITY
    # ------------------------------------------

    availability = DoctorAvailability.objects.get(
        id=availability_id,
        doctor=doctor
    )

    # ------------------------------------------
    # DELETE AVAILABILITY
    # ------------------------------------------

    if request.method == 'POST':

        availability.delete()

        return redirect(
            'doctor_availability'
        )

    # ------------------------------------------
    # DISPLAY DELETE CONFIRMATION
    # ------------------------------------------

    return render(
        request,
        'doctors/delete_availability.html',
        {
            'availability': availability
        }
    )
# ==========================================
# EDIT DOCTOR AVAILABILITY
# ==========================================

@login_required
@role_required('DOCTOR')
def edit_availability(request, availability_id):

    # ------------------------------------------
    # GET DOCTOR PROFILE
    # ------------------------------------------

    doctor = request.user.doctor_profile

    # ------------------------------------------
    # GET AVAILABILITY
    # ------------------------------------------

    availability = DoctorAvailability.objects.get(
        id=availability_id,
        doctor=doctor
    )

    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = DoctorAvailabilityForm(
            request.POST,
            instance=availability
        )

        if form.is_valid():

            form.save()

            return redirect(
                'doctor_availability'
            )

    # ------------------------------------------
    # DISPLAY EXISTING DATA
    # ------------------------------------------

    else:

        form = DoctorAvailabilityForm(
            instance=availability
        )

    # ------------------------------------------
    # RENDER EDIT PAGE
    # ------------------------------------------

    return render(
        request,
        'doctors/edit_availability.html',
        {
            'form': form,
            'availability': availability
        }
    )
# ==========================================
# DOCTOR SEARCH
# ==========================================

@login_required
@role_required('PATIENT')
def doctor_search(request):

    # ------------------------------------------
    # GET ALL ACTIVE DEPARTMENTS
    # ------------------------------------------

    departments = Department.objects.filter(
        is_active=True
    ).order_by('name')

    # ------------------------------------------
    # GET SELECTED DEPARTMENT
    # ------------------------------------------

    department_id = request.GET.get(
        'department'
    )

    # ------------------------------------------
    # GET AVAILABLE DOCTORS
    # ------------------------------------------

    doctors = Doctor.objects.filter(
        is_available=True
    ).select_related(
        'user',
        'department'
    )

    # ------------------------------------------
    # FILTER BY DEPARTMENT
    # ------------------------------------------

    if department_id:

        doctors = doctors.filter(
            department_id=department_id
        )

    # ------------------------------------------
    # RENDER SEARCH PAGE
    # ------------------------------------------

    return render(
        request,
        'doctors/search.html',
        {
            'departments': departments,
            'doctors': doctors,
            'selected_department': department_id,
        }
    )
# ==========================================
# DOCTOR DETAILS
# ==========================================

@login_required
@role_required('PATIENT')
def doctor_detail(request, doctor_id):

    # ------------------------------------------
    # GET DOCTOR
    # ------------------------------------------

    doctor = Doctor.objects.select_related(
        'user',
        'department'
    ).get(
        id=doctor_id,
        is_available=True
    )

    # ------------------------------------------
    # GET DOCTOR AVAILABILITY
    # ------------------------------------------

    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        is_active=True
    ).order_by(
        'day',
        'start_time'
    )

    # ------------------------------------------
    # RENDER DETAILS
    # ------------------------------------------

    return render(
        request,
        'doctors/detail.html',
        {
            'doctor': doctor,
            'availabilities': availabilities
        }
    )