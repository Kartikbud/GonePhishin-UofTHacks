from django.shortcuts import render
from .models import CallLog
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
def monitor_view(request):
    """View for the real-time monitoring page"""
    return render(request, 'detector/monitor.html')

@login_required
def history_view(request):
    """View to see past call analyses"""
    analyses = CallLog.objects.filter(user=request.user).order_by('-timestamp')
    for i in CallLog.objects.all():
        print(i.user)
    print(analyses)
    return render(request, 'detector/history.html', {'analyses': analyses})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'detector/login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'detector/login.html', {'error': 'Invalid email or password'})
    
    return render(request, 'detector/login.html')

def register_view(request):
    """View to register"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'detector/register.html', {'error': 'Invalid email address'})

        try:
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=name
            )
            user.save()
            return redirect('detector:login')
        except Exception as e:  # Changed to catch specific exception
            print(f"Error creating user: {e}")  # Added error logging
            return render(request, 'detector/register.html', {'error': 'Email already registered'})
    return render(request, 'detector/register.html')

@login_required
def signout_view(request):
    """View to sign out users"""
    logout(request)
    return redirect('/login')