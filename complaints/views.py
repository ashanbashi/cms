from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ComplaintForm, RegisterForm, CustomLoginForm
from .models import Complaint
from django.contrib import messages

# -------------------------------
# DASHBOARD
# -------------------------------
@login_required
def dashboard(request):
    # Show all complaints (current user first)
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'complaints': complaints, 'user': request.user})

# -------------------------------
# ADD COMPLAINT
# -------------------------------
@login_required
def add_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        messages.success(request, "Complaint submitted successfully!")
        return redirect('dashboard')
    return render(request, 'add_complaint.html', {'form': form})

# -------------------------------
# REGISTER
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# -------------------------------
# LOGIN
# -------------------------------
def login_user(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in!")
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
@login_required
def admin_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')  # Block normal users

    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'complaints': complaints})