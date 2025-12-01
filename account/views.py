from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Household, HouseholdMember

def get_user_household(user):
    return Household.objects.filter(
        HouseholdMember__user=user
    ).distinct()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/')
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('/')
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def account_settings(request):
    return render(request, 'account/account_settings.html')

@login_required
def household_settings(request):
    households = Household.objects.filter(
        householdmember__user=request.user
    ).distinct()
    return render(request, 'account/household_settings.html', {'households': households})
