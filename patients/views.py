from django.shortcuts import render, redirect
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
        {'form': form}
    )