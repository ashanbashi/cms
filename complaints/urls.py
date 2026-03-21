from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_complaint, name='add_complaint'),
    path('register/', views.register, name='register'),
]