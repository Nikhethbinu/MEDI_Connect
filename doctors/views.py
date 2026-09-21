from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import DoctorProfileForm
from .models import Doctor


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