from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, models
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.db import models
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('register_success')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'accounts/login.html')


def user_logout(request):

    logout(request)

    return redirect('login')

def register_success(request):
    return render(
        request,
        'accounts/register_success.html'
    )

# ==========================================
# MAIN DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    if request.user.role == 'PATIENT':
        return redirect('patient_dashboard')

    elif request.user.role == 'DOCTOR':
        return redirect('doctor_dashboard')

    elif request.user.role == 'ADMIN':
        return redirect('admin_dashboard')

    return redirect('login')


# ==========================================
# ROLE-BASED DASHBOARDS
# ==========================================

@login_required
@role_required('PATIENT')
def patient_dashboard(request):
    return render(
        request,
        'accounts/patient_dashboard.html'
    )


@login_required
@role_required('DOCTOR')
def doctor_dashboard(request):
    return render(
        request,
        'accounts/doctor_dashboard.html'
    )



# ==========================================
# ADMIN DASHBOARD
# ==========================================

@login_required
@role_required('ADMIN')
def admin_dashboard(request):

    # ------------------------------------------
    # IMPORT PROJECT MODELS
    # ------------------------------------------

    from doctors.models import (
        Doctor,
        Department
    )

    from patients.models import Patient

    from appointments.models import Appointment

    from prescriptions.models import Prescription

    from medical_records.models import MedicalRecord

    from billing.models import Payment


    # ==========================================
    # BASIC STATISTICS
    # ==========================================

    total_patients = Patient.objects.count()

    total_doctors = Doctor.objects.count()

    total_departments = Department.objects.count()

    total_appointments = Appointment.objects.count()


    # ==========================================
    # APPOINTMENT STATISTICS
    # ==========================================

    pending_appointments = Appointment.objects.filter(
        status='PENDING'
    ).count()

    confirmed_appointments = Appointment.objects.filter(
        status='CONFIRMED'
    ).count()

    completed_appointments = Appointment.objects.filter(
        status='COMPLETED'
    ).count()

    cancelled_appointments = Appointment.objects.filter(
        status='CANCELLED'
    ).count()

    rejected_appointments = Appointment.objects.filter(
        status='REJECTED'
    ).count()


    # ==========================================
    # PRESCRIPTION STATISTICS
    # ==========================================

    total_prescriptions = Prescription.objects.count()


    # ==========================================
    # MEDICAL RECORD STATISTICS
    # ==========================================

    total_medical_records = MedicalRecord.objects.count()


    # ==========================================
    # PAYMENT STATISTICS
    # ==========================================

    total_payments = Payment.objects.count()

    paid_payments = Payment.objects.filter(
        status='PAID'
    ).count()

    pending_payments = Payment.objects.filter(
        status='PENDING'
    ).count()


    # ==========================================
    # TOTAL REVENUE
    # ==========================================

    from django.db.models import Sum

    total_revenue = Payment.objects.filter(
        status='PAID'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0


    # ==========================================
    # RENDER DASHBOARD
    # ==========================================

    return render(
        request,
        'accounts/admin_dashboard.html',
        {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_departments': total_departments,
            'total_appointments': total_appointments,

            'pending_appointments':
                pending_appointments,

            'confirmed_appointments':
                confirmed_appointments,

            'completed_appointments':
                completed_appointments,

            'cancelled_appointments':
                cancelled_appointments,

            'rejected_appointments':
                rejected_appointments,

            'total_prescriptions':
                total_prescriptions,

            'total_medical_records':
                total_medical_records,

            'total_payments':
                total_payments,

            'paid_payments':
                paid_payments,

            'pending_payments':
                pending_payments,

            'total_revenue':
                total_revenue,
        }
    )

# ==========================================
# ADMIN - PATIENT MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_patients(request):

    from patients.models import Patient

    search_query = request.GET.get('search', '').strip()

    patients = Patient.objects.select_related(
        'user'
    ).order_by(
        'user__name'
    )

    if search_query:
        patients = patients.filter(
            models.Q(user__name__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(user__phone__icontains=search_query) |
            models.Q(user__email__icontains=search_query)
        )

    return render(
        request,
        'accounts/admin_patients.html',
        {
            'patients': patients,
            'search_query': search_query,
        }
    )
# ==========================================
# ADMIN - DOCTOR MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_doctors(request):

    from doctors.models import Doctor

    search_query = request.GET.get('search', '').strip()

    doctors = Doctor.objects.select_related(
        'user',
        'department'
    ).order_by(
        'user__name'
    )

    if search_query:
        doctors = doctors.filter(
            models.Q(user__name__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(user__phone__icontains=search_query) |
            models.Q(user__email__icontains=search_query) |
            models.Q(specialization__icontains=search_query) |
            models.Q(department__name__icontains=search_query)
        )

    return render(
        request,
        'accounts/admin_doctors.html',
        {
            'doctors': doctors,
            'search_query': search_query,
        }
    )

# ==========================================
# ADMIN - DEPARTMENT MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_departments(request):

    from doctors.models import Department
    from django.db.models import Count

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    departments = Department.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by(
        'name'
    )

    if search_query:

        departments = departments.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    return render(
        request,
        'accounts/admin_departments.html',
        {
            'departments': departments,
            'search_query': search_query,
        }
    )


# ==========================================
# ADMIN - ADD DEPARTMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_department_create(request):

    from doctors.forms import DepartmentForm

    if request.method == 'POST':

        form = DepartmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'admin_departments'
            )

    else:

        form = DepartmentForm()

    return render(
        request,
        'accounts/admin_department_form.html',
        {
            'form': form,
            'page_title': 'Add Department',
        }
    )


# ==========================================
# ADMIN - EDIT DEPARTMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_department_edit(request, department_id):

    from doctors.models import Department
    from doctors.forms import DepartmentForm

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == 'POST':

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            form.save()

            return redirect(
                'admin_departments'
            )

    else:

        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        'accounts/admin_department_form.html',
        {
            'form': form,
            'page_title': 'Edit Department',
            'department': department,
        }
    )


# ==========================================
# ADMIN - TOGGLE DEPARTMENT STATUS
# ==========================================

@login_required
@role_required('ADMIN')
def admin_department_toggle(request, department_id):

    from doctors.models import Department

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == 'POST':

        department.is_active = not department.is_active

        department.save(
            update_fields=['is_active']
        )

    return redirect(
        'admin_departments'
    )

# ==========================================
# ADMIN - APPOINTMENT MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_appointments(request):

    from appointments.models import Appointment

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    status_filter = request.GET.get(
        'status',
        ''
    ).strip()

    date_filter = request.GET.get(
        'date',
        ''
    ).strip()

    appointments = Appointment.objects.select_related(
        'patient',
        'doctor',
        'doctor__user',
        'doctor__department'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    # ==========================================
    # SEARCH BY PATIENT / DOCTOR
    # ==========================================

    if search_query:

        appointments = appointments.filter(
            models.Q(
                patient__name__icontains=search_query
            )
            |
            models.Q(
                patient__username__icontains=search_query
            )
            |
            models.Q(
                patient__phone__icontains=search_query
            )
            |
            models.Q(
                doctor__user__name__icontains=search_query
            )
            |
            models.Q(
                doctor__user__username__icontains=search_query
            )
            |
            models.Q(
                doctor__specialization__icontains=search_query
            )
        )

    # ==========================================
    # FILTER BY STATUS
    # ==========================================

    if status_filter:

        appointments = appointments.filter(
            status=status_filter
        )

    # ==========================================
    # FILTER BY DATE
    # ==========================================

    if date_filter:

        appointments = appointments.filter(
            appointment_date=date_filter
        )

    return render(
        request,
        'accounts/admin_appointments.html',
        {
            'appointments': appointments,
            'search_query': search_query,
            'status_filter': status_filter,
            'date_filter': date_filter,
        }
    )

# ==========================================
# ADMIN - PRESCRIPTION MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_prescriptions(request):

    from prescriptions.models import Prescription

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    prescriptions = Prescription.objects.select_related(
        'appointment',
        'appointment__patient',
        'appointment__doctor',
        'appointment__doctor__user'
    ).prefetch_related(
        'items',
        'items__medicine'
    ).order_by(
        '-created_at'
    )

    # ==========================================
    # SEARCH PRESCRIPTIONS
    # ==========================================

    if search_query:

        prescriptions = prescriptions.filter(
            models.Q(
                appointment__patient__name__icontains=search_query
            )
            |
            models.Q(
                appointment__patient__username__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__user__name__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__user__username__icontains=search_query
            )
            |
            models.Q(
                diagnosis__icontains=search_query
            )
            |
            models.Q(
                notes__icontains=search_query
            )
        )

    return render(
        request,
        'accounts/admin_prescriptions.html',
        {
            'prescriptions': prescriptions,
            'search_query': search_query,
        }
    )

# ==========================================
# ADMIN - MEDICAL RECORD MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_medical_records(request):

    from medical_records.models import MedicalRecord

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    date_filter = request.GET.get(
        'date',
        ''
    ).strip()

    records = MedicalRecord.objects.select_related(
        'patient',
        'appointment',
        'appointment__doctor',
        'appointment__doctor__user',
        'appointment__doctor__department'
    ).order_by(
        '-created_at'
    )

    # ==========================================
    # SEARCH
    # ==========================================

    if search_query:

        records = records.filter(
            models.Q(
                patient__name__icontains=search_query
            )
            |
            models.Q(
                patient__username__icontains=search_query
            )
            |
            models.Q(
                patient__phone__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__user__name__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__specialization__icontains=search_query
            )
            |
            models.Q(
                diagnosis__icontains=search_query
            )
            |
            models.Q(
                symptoms__icontains=search_query
            )
            |
            models.Q(
                treatment__icontains=search_query
            )
        )

    # ==========================================
    # DATE FILTER
    # ==========================================

    if date_filter:

        records = records.filter(
            appointment__appointment_date=date_filter
        )

    return render(
        request,
        'accounts/admin_medical_records.html',
        {
            'records': records,
            'search_query': search_query,
            'date_filter': date_filter,
        }
    )
# ==========================================
# ADMIN - PAYMENT MANAGEMENT
# ==========================================

@login_required
@role_required('ADMIN')
def admin_payments(request):

    from billing.models import Payment

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    status_filter = request.GET.get(
        'status',
        ''
    ).strip()

    method_filter = request.GET.get(
        'method',
        ''
    ).strip()

    payments = Payment.objects.select_related(
        'patient',
        'appointment',
        'appointment__doctor',
        'appointment__doctor__user',
        'appointment__doctor__department'
    ).order_by(
        '-created_at'
    )

    # ==========================================
    # SEARCH
    # ==========================================

    if search_query:

        payments = payments.filter(
            models.Q(
                patient__name__icontains=search_query
            )
            |
            models.Q(
                patient__username__icontains=search_query
            )
            |
            models.Q(
                patient__phone__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__user__name__icontains=search_query
            )
            |
            models.Q(
                appointment__doctor__user__username__icontains=search_query
            )
            |
            models.Q(
                transaction_id__icontains=search_query
            )
        )

    # ==========================================
    # STATUS FILTER
    # ==========================================

    if status_filter:

        payments = payments.filter(
            status=status_filter
        )

    # ==========================================
    # PAYMENT METHOD FILTER
    # ==========================================

    if method_filter:

        payments = payments.filter(
            payment_method=method_filter
        )

    return render(
        request,
        'accounts/admin_payments.html',
        {
            'payments': payments,
            'search_query': search_query,
            'status_filter': status_filter,
            'method_filter': method_filter,
        }
    )
# ==========================================
# ADMIN - REPORTS
# ==========================================

@login_required
@role_required('ADMIN')
def admin_reports(request):

    from django.db.models import Sum, Count

    from patients.models import Patient
    from doctors.models import Doctor, Department
    from appointments.models import Appointment
    from prescriptions.models import Prescription
    from medical_records.models import MedicalRecord
    from billing.models import Payment

    # ==========================================
    # BASIC STATISTICS
    # ==========================================

    total_patients = Patient.objects.count()

    total_doctors = Doctor.objects.count()

    total_departments = Department.objects.count()

    active_departments = Department.objects.filter(
        is_active=True
    ).count()

    total_appointments = Appointment.objects.count()

    total_prescriptions = Prescription.objects.count()

    total_medical_records = MedicalRecord.objects.count()

    total_payments = Payment.objects.count()

    # ==========================================
    # APPOINTMENT STATISTICS
    # ==========================================

    pending_appointments = Appointment.objects.filter(
        status='PENDING'
    ).count()

    confirmed_appointments = Appointment.objects.filter(
        status='CONFIRMED'
    ).count()

    rejected_appointments = Appointment.objects.filter(
        status='REJECTED'
    ).count()

    cancelled_appointments = Appointment.objects.filter(
        status='CANCELLED'
    ).count()

    completed_appointments = Appointment.objects.filter(
        status='COMPLETED'
    ).count()

    # ==========================================
    # PAYMENT STATISTICS
    # ==========================================

    pending_payments = Payment.objects.filter(
        status='PENDING'
    ).count()

    paid_payments = Payment.objects.filter(
        status='PAID'
    ).count()

    failed_payments = Payment.objects.filter(
        status='FAILED'
    ).count()

    cancelled_payments = Payment.objects.filter(
        status='CANCELLED'
    ).count()

    # ==========================================
    # REVENUE
    # ==========================================

    total_revenue = Payment.objects.filter(
        status='PAID'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    pending_revenue = Payment.objects.filter(
        status='PENDING'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # ==========================================
    # DEPARTMENT-WISE DOCTOR COUNT
    # ==========================================

    department_reports = Department.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by(
        'name'
    )

    # ==========================================
    # PAYMENT METHOD STATISTICS
    # ==========================================

    cash_payments = Payment.objects.filter(
        payment_method='CASH'
    ).count()

    card_payments = Payment.objects.filter(
        payment_method='CARD'
    ).count()

    upi_payments = Payment.objects.filter(
        payment_method='UPI'
    ).count()

    net_banking_payments = Payment.objects.filter(
        payment_method='NET_BANKING'
    ).count()

    return render(
        request,
        'accounts/admin_reports.html',
        {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_departments': total_departments,
            'active_departments': active_departments,
            'total_appointments': total_appointments,
            'total_prescriptions': total_prescriptions,
            'total_medical_records': total_medical_records,
            'total_payments': total_payments,

            'pending_appointments': pending_appointments,
            'confirmed_appointments': confirmed_appointments,
            'rejected_appointments': rejected_appointments,
            'cancelled_appointments': cancelled_appointments,
            'completed_appointments': completed_appointments,

            'pending_payments': pending_payments,
            'paid_payments': paid_payments,
            'failed_payments': failed_payments,
            'cancelled_payments': cancelled_payments,

            'total_revenue': total_revenue,
            'pending_revenue': pending_revenue,

            'department_reports': department_reports,

            'cash_payments': cash_payments,
            'card_payments': card_payments,
            'upi_payments': upi_payments,
            'net_banking_payments': net_banking_payments,
        }
    )