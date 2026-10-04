from decimal import Decimal

from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.utils import timezone

from accounts.decorators import role_required

from doctors.models import Doctor

from appointments.models import Appointment

from .models import Payment

from .forms import PaymentForm


# ==========================================
# CREATE PAYMENT / BILL
# ==========================================

@login_required
@role_required('DOCTOR')
def create_payment(request, appointment_id):

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
    # CHECK EXISTING PAYMENT
    # ------------------------------------------

    if hasattr(appointment, 'payment'):

        return redirect(
            'payment_detail',
            payment_id=appointment.payment.id
        )

    # ------------------------------------------
    # DEFAULT CONSULTATION FEE
    # ------------------------------------------

    initial_data = {
        'consultation_fee':
            appointment.doctor.consultation_fee,
        'additional_charges': Decimal('0.00'),
    }

    # ------------------------------------------
    # HANDLE FORM SUBMISSION
    # ------------------------------------------

    if request.method == 'POST':

        form = PaymentForm(
            request.POST
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            # ------------------------------------------
            # CONNECT APPOINTMENT
            # ------------------------------------------

            payment.appointment = appointment

            # ------------------------------------------
            # CONNECT PATIENT
            # ------------------------------------------

            payment.patient = appointment.patient

            # ------------------------------------------
            # CALCULATE TOTAL
            # ------------------------------------------

            payment.total_amount = (
                payment.consultation_fee
                + payment.additional_charges
            )

            # ------------------------------------------
            # PAYMENT DATE
            # ------------------------------------------

            if payment.status == 'PAID':

                payment.payment_date = timezone.now()

            payment.save()

            return redirect(
                'payment_detail',
                payment_id=payment.id
            )

    else:

        form = PaymentForm(
            initial=initial_data
        )

    # ------------------------------------------
    # RENDER
    # ------------------------------------------

    return render(
        request,
        'billing/create.html',
        {
            'appointment': appointment,
            'form': form,
        }
    )


# ==========================================
# PAYMENT DETAIL
# ==========================================

@login_required
def payment_detail(
    request,
    payment_id
):

    # ------------------------------------------
    # GET PAYMENT
    # ------------------------------------------

    payment = get_object_or_404(
        Payment.objects.select_related(
            'patient',
            'appointment',
            'appointment__doctor',
            'appointment__doctor__user',
        ),
        id=payment_id
    )

    # ------------------------------------------
    # DOCTOR ACCESS
    # ------------------------------------------

    if request.user.role == 'DOCTOR':

        if (
            payment.appointment.doctor.user
            != request.user
        ):

            return redirect(
                'dashboard'
            )

    # ------------------------------------------
    # PATIENT ACCESS
    # ------------------------------------------

    elif request.user.role == 'PATIENT':

        if payment.patient != request.user:

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
        'billing/detail.html',
        {
            'payment': payment,
        }
    )


# ==========================================
# PATIENT PAYMENT HISTORY
# ==========================================

@login_required
@role_required('PATIENT')
def patient_payments(request):

    payments = Payment.objects.filter(
        patient=request.user
    ).select_related(
        'appointment',
        'appointment__doctor',
        'appointment__doctor__user'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'billing/patient_payments.html',
        {
            'payments': payments,
        }
    )