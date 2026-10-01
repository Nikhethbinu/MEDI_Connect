from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from accounts.decorators import role_required

from doctors.models import Doctor

from appointments.models import Appointment

from .models import (
    Prescription,
    PrescriptionItem
)

from .forms import (
    PrescriptionForm,
    PrescriptionItemFormSet
)


# ==========================================
# CREATE PRESCRIPTION
# ==========================================

@login_required
@role_required('DOCTOR')
def create_prescription(request, appointment_id):

    # ------------------------------------------
    # GET LOGGED-IN DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET COMPLETED APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor,
        status='COMPLETED'
    )

    # ------------------------------------------
    # CHECK EXISTING PRESCRIPTION
    # ------------------------------------------

    if hasattr(appointment, 'prescription'):

        return redirect(
            'prescription_detail',
            prescription_id=appointment.prescription.id
        )

    # ------------------------------------------
    # HANDLE SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        prescription_form = PrescriptionForm(
            request.POST
        )

        item_formset = PrescriptionItemFormSet(
            request.POST
        )

        if (
            prescription_form.is_valid()
            and item_formset.is_valid()
        ):

            # ------------------------------------------
            # CREATE PRESCRIPTION
            # ------------------------------------------

            prescription = prescription_form.save(
                commit=False
            )

            prescription.appointment = appointment

            prescription.save()

            # ------------------------------------------
            # CREATE MEDICINE ITEMS
            # ------------------------------------------

            items = item_formset.save(
                commit=False
            )

            for item in items:

                item.prescription = prescription

                item.save()

            # ------------------------------------------
            # DELETE MARKED ITEMS
            # ------------------------------------------

            for item in item_formset.deleted_objects:

                item.delete()

            # ------------------------------------------
            # REDIRECT
            # ------------------------------------------

            return redirect(
                'prescription_detail',
                prescription_id=prescription.id
            )

    else:

        prescription_form = PrescriptionForm()

        item_formset = PrescriptionItemFormSet()

    # ------------------------------------------
    # RENDER PAGE
    # ------------------------------------------

    return render(
        request,
        'prescriptions/create.html',
        {
            'appointment': appointment,
            'prescription_form': prescription_form,
            'item_formset': item_formset,
        }
    )

# ==========================================
# PRESCRIPTION DETAIL
# ==========================================

@login_required
def prescription_detail(
    request,
    prescription_id
):

    # ------------------------------------------
    # GET PRESCRIPTION
    # ------------------------------------------

    prescription = get_object_or_404(
        Prescription.objects.select_related(
            'appointment',
            'appointment__patient',
            'appointment__doctor',
            'appointment__doctor__user'
        ).prefetch_related(
            'items',
            'items__medicine'
        ),
        id=prescription_id
    )

    # ------------------------------------------
    # ACCESS CONTROL
    # ------------------------------------------

    if request.user.role == 'DOCTOR':

        if prescription.appointment.doctor.user != request.user:

            return redirect('dashboard')

    elif request.user.role == 'PATIENT':

        if prescription.appointment.patient != request.user:

            return redirect('dashboard')

    else:

        return redirect('dashboard')

    # ------------------------------------------
    # RENDER PRESCRIPTION
    # ------------------------------------------

    return render(
        request,
        'prescriptions/detail.html',
        {
            'prescription': prescription
        }
    )
# ==========================================
# EDIT PRESCRIPTION
# ==========================================

@login_required
@role_required('DOCTOR')
def edit_prescription(request, prescription_id):

    # ------------------------------------------
    # GET LOGGED-IN DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET PRESCRIPTION
    # ------------------------------------------

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id,
        appointment__doctor=doctor
    )

    # ------------------------------------------
    # GET APPOINTMENT
    # ------------------------------------------

    appointment = prescription.appointment

    # ------------------------------------------
    # ONLY COMPLETED APPOINTMENTS
    # ------------------------------------------

    if appointment.status != 'COMPLETED':

        return redirect(
            'doctor_appointments'
        )

    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        prescription_form = PrescriptionForm(
            request.POST,
            instance=prescription
        )

        item_formset = PrescriptionItemFormSet(
            request.POST,
            instance=prescription
        )

        # ------------------------------------------
        # VALIDATE FORMS
        # ------------------------------------------

        if (
            prescription_form.is_valid()
            and item_formset.is_valid()
        ):

            # ------------------------------------------
            # UPDATE PRESCRIPTION
            # ------------------------------------------

            prescription_form.save()

            # ------------------------------------------
            # UPDATE / ADD / DELETE MEDICINES
            # ------------------------------------------

            item_formset.save()

            # ------------------------------------------
            # REDIRECT TO DETAIL PAGE
            # ------------------------------------------

            return redirect(
                'prescription_detail',
                prescription_id=prescription.id
            )

    # ------------------------------------------
    # DISPLAY EXISTING DATA
    # ------------------------------------------

    else:

        prescription_form = PrescriptionForm(
            instance=prescription
        )

        item_formset = PrescriptionItemFormSet(
            instance=prescription
        )

    # ------------------------------------------
    # RENDER EDIT PAGE
    # ------------------------------------------

    return render(
        request,
        'prescriptions/edit.html',
        {
            'appointment': appointment,
            'prescription': prescription,
            'prescription_form': prescription_form,
            'item_formset': item_formset,
        }
    )