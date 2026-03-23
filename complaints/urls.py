from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ----------------- FIRST PAGE / REGISTER -----------------
    path('', views.register, name='register'),  # Root URL shows register page

    # ----------------- LOGIN -----------------
    path('login/', views.login_user, name='login'),

    # ----------------- LOGOUT -----------------
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ----------------- DASHBOARD (Normal User) -----------------
    path('dashboard/', views.dashboard, name='dashboard'),

    # ----------------- ADMIN DASHBOARD -----------------
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # ----------------- ADD COMPLAINT -----------------
    path('add-complaint/', views.add_complaint, name='add_complaint'),

     # AJAX endpoint for status update
    path('update_status/', views.update_complaint_status, name='update_status'),


     # ----------------- BUTTONS -----------------
    path('like/', views.toggle_like, name='toggle_like'),

    path('delete/', views.delete_complaint, name='delete_complaint'),
]