from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PatientProfileForm
from .models import Patient


# ==========================================
# PATIENT PROFILE
# ==========================================

@login_required
def patient_profile(request):

    # ------------------------------------------
    # GET EXISTING PATIENT PROFILE
    # ------------------------------------------

    try:
        patient = request.user.patient_profile

    except Patient.DoesNotExist:
        patient = None


    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = PatientProfileForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():

            # ------------------------------------------
            # SAVE PATIENT PROFILE
            # ------------------------------------------

            patient = form.save(commit=False)

            patient.user = request.user

            patient.save()

            return redirect('patient_profile')


    # ------------------------------------------
    # DISPLAY PROFILE FORM
    # ------------------------------------------

    else:

        form = PatientProfileForm(
            instance=patient
        )


    # ------------------------------------------
    # RENDER PROFILE PAGE
    # ------------------------------------------

    return render(
        request,
        'patients/profile.html',
        {
            'form': form,
            'patient': patient
        }
    )


# ==========================================
# EDIT PATIENT PROFILE
# ==========================================

@login_required
def edit_patient_profile(request):

    # ------------------------------------------
    # GET EXISTING PATIENT PROFILE
    # ------------------------------------------

    try:
        patient = request.user.patient_profile

    except Patient.DoesNotExist:
        patient = None


    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = PatientProfileForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():

            # ------------------------------------------
            # SAVE PATIENT PROFILE
            # ------------------------------------------

            patient = form.save(commit=False)

            patient.user = request.user

            patient.save()

            return redirect('patient_profile')


    # ------------------------------------------
    # DISPLAY EXISTING PROFILE
    # ------------------------------------------

    else:

        form = PatientProfileForm(
            instance=patient
        )


    # ------------------------------------------
    # RENDER EDIT PROFILE PAGE
    # ------------------------------------------

    return render(
        request,
        'patients/edit_profile.html',
        {
            'form': form,
            'patient': patient
        }
    )