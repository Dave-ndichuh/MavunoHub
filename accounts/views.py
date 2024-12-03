from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseForbidden
from .forms import SignupForm, LoginForm
from .models import UserProfile


# Custom decorators for user type authorization
def user_is_farmer(function):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.user_type != 'farmer':
            return HttpResponseForbidden("You are not authorized to access this page")
        return function(request, *args, **kwargs)
    return _wrapped_view

def user_is_customer(function):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.user_type != 'customer':
            return HttpResponseForbidden("You are not authorized to access this page")
        return function(request, *args, **kwargs)
    return _wrapped_view

def user_is_admin(function):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.user_type != 'admin':
            return HttpResponseForbidden("You are not authorized to access this page")
        return function(request, *args, **kwargs)
    return _wrapped_view


# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately

            # Redirect based on the user type
            if user.profile.user_type == 'farmer':
                return redirect('farmer_dashboard')
            elif user.profile.user_type == 'customer':
                return redirect('customer_dashboard')
            elif user.profile.user_type == 'admin':
                return redirect('admin_dashboard')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Redirect based on user type
                if user.profile.user_type == 'farmer':
                    return redirect('farmer_dashboard')
                elif user.profile.user_type == 'customer':
                    return redirect('customer_dashboard')
                elif user.profile.user_type == 'admin':
                    return redirect('admin_dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Dashboard Views

# Farmer Dashboard (only accessible by farmers)
@user_is_farmer
@login_required
def farmer_dashboard(request):
    return render(request, 'farmer_dashboard.html')

# Customer Dashboard (only accessible by customers)
@user_is_customer
@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

# Admin Dashboard (only accessible by admins)
@user_is_admin
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


# View for logout
def logout_view(request):
    logout(request)
    return redirect('login')
