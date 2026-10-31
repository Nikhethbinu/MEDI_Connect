from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from accounts.decorators import role_required
from django.views.decorators.http import require_POST
from doctors.models import Doctor, DoctorAvailability

from .forms import AppointmentForm
from .models import Appointment
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from datetime import datetime, timedelta

# ==========================================
# BOOK APPOINTMENT - DATE-BASED AVAILABILITY
# ==========================================

from django.utils import timezone

# ==========================================
# GET AVAILABLE 15-MINUTE SLOTS
# ==========================================

@login_required
@role_required('PATIENT')
def available_slots(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id,
        is_available=True
    )

    selected_date = request.GET.get('date')

    if not selected_date:
        return JsonResponse({
            'slots': [],
            'message': 'Please select an appointment date.'
        })

    try:
        appointment_date = datetime.strptime(
            selected_date,
            '%Y-%m-%d'
        ).date()
    except ValueError:
        return JsonResponse({
            'slots': [],
            'message': 'Invalid appointment date.'
        }, status=400)

    today = timezone.localdate()

    if appointment_date < today:
        return JsonResponse({
            'slots': [],
            'message': 'Appointment date cannot be in the past.'
        })

    # Check whether this patient already has an appointment
    # with this doctor on the selected date.
    existing_patient_booking = Appointment.objects.filter(
        patient=request.user,
        doctor=doctor,
        appointment_date=appointment_date
    ).exclude(
        status__in=['CANCELLED', 'REJECTED']
    ).exists()

    if existing_patient_booking:
        return JsonResponse({
            'slots': [],
            'message': 'You already have an appointment with this doctor on this date.'
        })

    # Get the doctor's active availability for this date.
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        availability_date=appointment_date,
        is_active=True
    ).order_by('start_time')

    # Existing appointment times are unavailable.
    booked_times = set(
        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date
        ).values_list(
            'appointment_time',
            flat=True
        )
    )

    slots = []
    now = timezone.localtime()

    for availability in availabilities:

        slot_start = datetime.combine(
            appointment_date,
            availability.start_time
        )

        availability_end = datetime.combine(
            appointment_date,
            availability.end_time
        )

        lunch_start = datetime.combine(
            appointment_date,
            doctor.lunch_start_time
        )

        lunch_end = datetime.combine(
            appointment_date,
            doctor.lunch_end_time
        )

        while slot_start + timedelta(minutes=15) <= availability_end:

            slot_end = slot_start + timedelta(minutes=15)

            # Exclude slots that overlap the lunch break.
            overlaps_lunch = (
                slot_start < lunch_end
                and slot_end > lunch_start
            )

            # Exclude past slots.
            is_past = (
                appointment_date == today
                and slot_start <= now.replace(tzinfo=None)
            )

            slot_time = slot_start.time()

            if (
                not overlaps_lunch
                and not is_past
                and slot_time not in booked_times
            ):
                slots.append(
                    slot_time.strftime('%H:%M')
                )

            slot_start = slot_end

    return JsonResponse({
        'slots': sorted(set(slots)),
        'message': (
            'Available appointment slots.'
            if slots
            else 'No appointment slots are available for this date.'
        )
    })
@login_required
@role_required('PATIENT')
def book_appointment(request, doctor_id):

    # ==========================================
    # GET DOCTOR
    # ==========================================

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id,
        is_available=True
    )

    # ==========================================
    # GET UPCOMING DOCTOR AVAILABILITY
    # ==========================================

    today = timezone.localdate()

    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        availability_date__gte=today,
        is_active=True
    ).order_by(
        'availability_date',
        'start_time'
    )

    # ==========================================
    # HANDLE FORM SUBMISSION
    # ==========================================

    if request.method == 'POST':

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']

            # ==========================================
            # CHECK THAT APPOINTMENT IS NOT IN THE PAST
            # ==========================================

            current_time = timezone.localtime().time()

            if (
                appointment_date < today
                or (
                    appointment_date == today
                    and appointment_time <= current_time
                )
            ):

                form.add_error(
                    None,
                    'Please select a future appointment date and time.'
                )

            # ==========================================
            # CHECK 15-MINUTE INTERVAL
            # ==========================================

            elif (
                appointment_time.minute % 15 != 0
                or appointment_time.second != 0
            ):

                form.add_error(
                    'appointment_time',
                    'Please select a valid 15-minute appointment slot.'
                )

            else:

                slot_start = datetime.combine(
                    appointment_date,
                    appointment_time
                )

                slot_end = slot_start + timedelta(minutes=15)

                # ==========================================
                # CHECK PATIENT DAILY BOOKING LIMIT
                # ==========================================

                existing_patient_booking = Appointment.objects.filter(
                    patient=request.user,
                    doctor=doctor,
                    appointment_date=appointment_date
                ).exclude(
                    status__in=['CANCELLED', 'REJECTED']
                ).exists()

                if existing_patient_booking:

                    form.add_error(
                        None,
                        'You already have an appointment with this doctor on this date.'
                    )

                else:

                    # ==========================================
                    # CHECK DOCTOR AVAILABILITY
                    # ==========================================

                    availability = DoctorAvailability.objects.filter(
                        doctor=doctor,
                        availability_date=appointment_date,
                        is_active=True,
                        start_time__lte=appointment_time,
                        end_time__gte=slot_end.time()
                    ).first()

                    if not availability:

                        form.add_error(
                            None,
                            'The doctor is not available for the selected time.'
                        )

                    else:

                        # ==========================================
                        # CHECK LUNCH BREAK
                        # ==========================================

                        lunch_start = datetime.combine(
                            appointment_date,
                            doctor.lunch_start_time
                        )

                        lunch_end = datetime.combine(
                            appointment_date,
                            doctor.lunch_end_time
                        )

                        if (
                            slot_start < lunch_end
                            and slot_end > lunch_start
                        ):

                            form.add_error(
                                'appointment_time',
                                'This time overlaps the doctor\'s lunch break.'
                            )

                        else:

                            # ==========================================
                            # CHECK DOUBLE BOOKING
                            # ==========================================

                            existing_appointment = Appointment.objects.filter(
                                doctor=doctor,
                                appointment_date=appointment_date,
                                appointment_time=appointment_time
                            ).exists()

                            if existing_appointment:

                                form.add_error(
                                    'appointment_time',
                                    'This appointment slot is already booked.'
                                )

                            else:

                                # ==========================================
                                # CREATE APPOINTMENT
                                # ==========================================

                                appointment = form.save(commit=False)

                                appointment.patient = request.user
                                appointment.doctor = doctor
                                appointment.status = 'PENDING'

                                try:

                                    with transaction.atomic():
                                        appointment.save()

                                except IntegrityError:

                                    form.add_error(
                                        None,
                                        'This appointment slot is already booked. '
                                        'Please select another date or time.'
                                    )

                                else:

                                    return redirect(
                                        'appointment_success',
                                        appointment_id=appointment.id
                                    )

    else:

        form = AppointmentForm()

    # ==========================================
    # RENDER BOOKING PAGE
    # ==========================================

    return render(
        request,
        'appointments/book.html',
        {
            'form': form,
            'doctor': doctor,
            'availabilities': availabilities
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
        'doctor__user'
    ).order_by(
        '-created_at'
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
@require_POST
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
@require_POST
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
@require_POST
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
@require_POST
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