from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ComplaintForm, RegisterForm
from .models import Complaint

@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'complaints': complaints})

@login_required
def add_complaint(request):
    form = ComplaintForm(request.POST or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        return redirect('dashboard')
    return render(request, 'add_complaint.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})