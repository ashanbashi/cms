from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ComplaintForm, RegisterForm, CustomLoginForm
from .models import Complaint
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q


# -------------------------------
# DASHBOARD
# -------------------------------
@login_required
def dashboard(request):
    sort = request.GET.get('sort')
    query = request.GET.get('q', '').strip()

    # 🔥 Split complaints
    my_complaints = Complaint.objects.filter(user=request.user)
    other_complaints = Complaint.objects.exclude(user=request.user)

    # 🔍 APPLY SEARCH TO BOTH
    if query:
        my_complaints = my_complaints.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        other_complaints = other_complaints.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Sorting
    if sort == 'newest':
        my_complaints = my_complaints.order_by('-created_at')
        other_complaints = other_complaints.order_by('-created_at')
    elif sort == 'oldest':
        my_complaints = my_complaints.order_by('created_at')
        other_complaints = other_complaints.order_by('created_at')
    else:
        my_complaints = my_complaints.order_by('-created_at')
        other_complaints = other_complaints.order_by('-created_at')

    return render(request, 'dashboard.html', {
        'my_complaints': my_complaints,
        'other_complaints': other_complaints,
    })
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
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied 🚫")
        return redirect('dashboard')

    status_filter = request.GET.get('status', 'all')
    complaints = Complaint.objects.all()

    if status_filter.lower() != 'all':
        complaints = complaints.filter(status=status_filter.title())

    return render(request, 'admin_dashboard.html', {'complaints': complaints})

@login_required
def update_complaint_status(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        complaint_id = request.POST.get('id')
        new_status = request.POST.get('status')
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.status = new_status
            complaint.save()
            return JsonResponse({'success': True})
        except Complaint.DoesNotExist:
            return JsonResponse({'error': 'Complaint not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_like(request):
    if request.method == "POST":
        complaint_id = request.POST.get('id')
        complaint = Complaint.objects.get(id=complaint_id)

        if request.user in complaint.likes.all():
            complaint.likes.remove(request.user)
            liked = False
        else:
            complaint.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'count': complaint.likes.count()
        })
    

@login_required
def delete_complaint(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == "POST":
        complaint_id = request.POST.get('id')
        Complaint.objects.filter(id=complaint_id).delete()
        return JsonResponse({'success': True})