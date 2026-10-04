from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required

from doctors.models import Doctor, DoctorAvailability

from .forms import AppointmentForm
from .models import Appointment


# ==========================================
# BOOK APPOINTMENT
# ==========================================

@login_required
@role_required('PATIENT')
def book_appointment(request, doctor_id):

    # ------------------------------------------
    # GET DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
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
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = AppointmentForm(
            request.POST
        )

        if form.is_valid():

            appointment_date = (
                form.cleaned_data['appointment_date']
            )

            appointment_time = (
                form.cleaned_data['appointment_time']
            )

            # ------------------------------------------
            # CHECK DOCTOR'S AVAILABLE DAY
            # ------------------------------------------

            day_name = appointment_date.strftime(
                '%A'
            ).upper()

            availability = (
                DoctorAvailability.objects.filter(
                    doctor=doctor,
                    day=day_name,
                    is_active=True
                )
                .filter(
                    start_time__lte=appointment_time,
                    end_time__gte=appointment_time
                )
                .first()
            )

            if not availability:

                form.add_error(
                    None,
                    'Doctor is not available at the selected date and time.'
                )

            else:

                # ------------------------------------------
                # CHECK DOUBLE BOOKING
                # ------------------------------------------

                existing_appointment = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    status__in=[
                        'PENDING',
                        'CONFIRMED'
                    ]
                ).exists()

                if existing_appointment:

                    form.add_error(
                        None,
                        'This appointment slot is already booked.'
                    )

                else:

                    # ------------------------------------------
                    # CREATE APPOINTMENT
                    # ------------------------------------------

                    appointment = form.save(
                        commit=False
                    )

                    appointment.patient = request.user

                    appointment.doctor = doctor

                    appointment.status = 'PENDING'

                    appointment.save()

                    return redirect(
                        'appointment_success',
                        appointment_id=appointment.id
                    )

    else:

        form = AppointmentForm()

    # ------------------------------------------
    # RENDER BOOKING PAGE
    # ------------------------------------------

    return render(
        request,
        'appointments/book.html',
        {
            'form': form,
            'doctor': doctor,
            'availabilities': availabilities,
        }
    )
# ==========================================
# APPOINTMENT SUCCESS
# ==========================================

@login_required
@role_required('PATIENT')
def appointment_success(
    request,
    appointment_id
):

    # ------------------------------------------
    # GET PATIENT'S APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    # ------------------------------------------
    # RENDER SUCCESS PAGE
    # ------------------------------------------

    return render(
        request,
        'appointments/success.html',
        {
            'appointment': appointment
        }
    )
# ==========================================
# PATIENT APPOINTMENT HISTORY
# ==========================================

@login_required
@role_required('PATIENT')
def appointment_history(request):

    # ------------------------------------------
    # GET PATIENT APPOINTMENTS
    # ------------------------------------------

    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related(
        'doctor',
        'doctor__user',
        'doctor__department'
    ).prefetch_related(
        'prescription'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    # ------------------------------------------
    # CHECK PRESCRIPTION
    # ------------------------------------------

    for appointment in appointments:

        try:
            prescription = appointment.prescription

            appointment.has_prescription = True
            appointment.prescription_id_value = prescription.id

        except Appointment.prescription.RelatedObjectDoesNotExist:
            appointment.has_prescription = False
            appointment.prescription_id_value = None

    # ------------------------------------------
    # RENDER HISTORY
    # ------------------------------------------

    return render(
        request,
        'appointments/history.html',
        {
            'appointments': appointments
        }
    )

# ==========================================
# CANCEL APPOINTMENT
# ==========================================

@login_required
@role_required('PATIENT')
def cancel_appointment(request, appointment_id):

    # ------------------------------------------
    # GET PATIENT'S APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    # ------------------------------------------
    # CANCEL APPOINTMENT
    # ------------------------------------------

    if request.method == 'POST':

        if appointment.status in [
            'PENDING',
            'CONFIRMED'
        ]:
            appointment.status = 'CANCELLED'
            appointment.save()

        return redirect('appointment_history')

    # ------------------------------------------
    # RENDER CONFIRMATION PAGE
    # ------------------------------------------

    return render(
        request,
        'appointments/cancel.html',
        {
            'appointment': appointment
        }
    )

# ==========================================
# DOCTOR APPOINTMENTS
# ==========================================

@login_required
@role_required('DOCTOR')
def doctor_appointments(request):

    # ------------------------------------------
    # GET LOGGED-IN DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET DOCTOR APPOINTMENTS
    # ------------------------------------------

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        'patient',
        'doctor',
        'doctor__department'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    # ------------------------------------------
    # CHECK PRESCRIPTION AND MEDICAL RECORD
    # ------------------------------------------

    for appointment in appointments:

        # ==========================================
        # PRESCRIPTION
        # ==========================================

        try:

            prescription = appointment.prescription

            appointment.has_prescription = True

            appointment.prescription_id_value = (
                prescription.id
            )

        except Appointment.prescription.RelatedObjectDoesNotExist:

            appointment.has_prescription = False

            appointment.prescription_id_value = None


        # ==========================================
        # MEDICAL RECORD
        # ==========================================

        try:

            medical_record = appointment.medical_record

            appointment.has_medical_record = True

            appointment.medical_record_id_value = (
                medical_record.id
            )

        except Appointment.medical_record.RelatedObjectDoesNotExist:

            appointment.has_medical_record = False

            appointment.medical_record_id_value = None
        
        # ==========================================
        # PAYMENT
        # ==========================================

        try:

            payment = appointment.payment

            appointment.has_payment = True

            appointment.payment_id_value = (
                payment.id
            )

        except Appointment.payment.RelatedObjectDoesNotExist:

            appointment.has_payment = False

            appointment.payment_id_value = None


    # ------------------------------------------
    # RENDER
    # ------------------------------------------

    return render(
        request,
        'appointments/doctor_appointments.html',
        {
            'appointments': appointments
        }
    )

# ==========================================
# CONFIRM APPOINTMENT
# ==========================================

@login_required
@role_required('DOCTOR')
def confirm_appointment(request, appointment_id):

    # ------------------------------------------
    # GET DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # ------------------------------------------
    # CONFIRM ONLY PENDING APPOINTMENTS
    # ------------------------------------------

    if request.method == 'POST':

        if appointment.status == 'PENDING':

            appointment.status = 'CONFIRMED'
            appointment.save()

    return redirect('doctor_appointments')


# ==========================================
# REJECT APPOINTMENT
# ==========================================

@login_required
@role_required('DOCTOR')
def reject_appointment(request, appointment_id):

    # ------------------------------------------
    # GET DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # ------------------------------------------
    # REJECT ONLY PENDING APPOINTMENTS
    # ------------------------------------------

    if request.method == 'POST':

        if appointment.status == 'PENDING':

            appointment.status = 'REJECTED'
            appointment.save()

    return redirect('doctor_appointments')


# ==========================================
# COMPLETE APPOINTMENT
# ==========================================

@login_required
@role_required('DOCTOR')
def complete_appointment(request, appointment_id):

    # ------------------------------------------
    # GET DOCTOR
    # ------------------------------------------

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    # ------------------------------------------
    # GET APPOINTMENT
    # ------------------------------------------

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # ------------------------------------------
    # COMPLETE ONLY CONFIRMED APPOINTMENTS
    # ------------------------------------------

    if request.method == 'POST':

        if appointment.status == 'CONFIRMED':

            appointment.status = 'COMPLETED'
            appointment.save()

    return redirect('doctor_appointments')