from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required

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



@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    return render(
        request,
        'accounts/admin_dashboard.html'
    )