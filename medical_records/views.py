from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from accounts.decorators import role_required

from doctors.models import Doctor

from appointments.models import Appointment

from .models import MedicalRecord

from .forms import MedicalRecordForm


# ==========================================
# CREATE MEDICAL RECORD
# ==========================================

@login_required
@role_required('DOCTOR')
def create_medical_record(
    request,
    appointment_id
):

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
    # CHECK EXISTING RECORD
    # ------------------------------------------

    if hasattr(
        appointment,
        'medical_record'
    ):

        return redirect(
            'medical_record_detail',
            record_id=appointment.medical_record.id
        )

    # ------------------------------------------
    # HANDLE FORM
    # ------------------------------------------

    if request.method == 'POST':

        form = MedicalRecordForm(
            request.POST
        )

        if form.is_valid():

            record = form.save(
                commit=False
            )

            record.patient = appointment.patient

            record.appointment = appointment

            record.save()

            return redirect(
                'medical_record_detail',
                record_id=record.id
            )

    else:

        form = MedicalRecordForm()

    # ------------------------------------------
    # RENDER
    # ------------------------------------------

    return render(
        request,
        'medical_records/create.html',
        {
            'appointment': appointment,
            'form': form,
        }
    )


# ==========================================
# MEDICAL RECORD DETAIL
# ==========================================

@login_required
def medical_record_detail(
    request,
    record_id
):

    # ------------------------------------------
    # GET RECORD
    # ------------------------------------------

    record = get_object_or_404(
        MedicalRecord.objects.select_related(
            'patient',
            'appointment',
            'appointment__doctor',
            'appointment__doctor__user',
        ),
        id=record_id
    )

    # ------------------------------------------
    # DOCTOR ACCESS
    # ------------------------------------------

    if request.user.role == 'DOCTOR':

        if (
            record.appointment.doctor.user
            != request.user
        ):

            return redirect(
                'dashboard'
            )

    # ------------------------------------------
    # PATIENT ACCESS
    # ------------------------------------------

    elif request.user.role == 'PATIENT':

        if record.patient != request.user:

            return redirect(
                'dashboard'
            )

    # ------------------------------------------
    # OTHER ROLES
    # ------------------------------------------

    else:

        return redirect(
            'dashboard'
        )

    # ------------------------------------------
    # RENDER
    # ------------------------------------------

    return render(
        request,
        'medical_records/detail.html',
        {
            'record': record,
        }
    )


# ==========================================
# PATIENT MEDICAL RECORDS
# ==========================================

@login_required
@role_required('PATIENT')
def patient_medical_records(request):

    records = MedicalRecord.objects.filter(
        patient=request.user
    ).select_related(
        'appointment',
        'appointment__doctor',
        'appointment__doctor__user',
        'appointment__doctor__department'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'medical_records/patient_records.html',
        {
            'records': records,
        }
    )