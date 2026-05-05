from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import CreateUserForm, UserChangePasswordForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash


def home(request):
    context = {}
    return render(request, 'accounts/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('accounts:my-login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def my_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')  # Username / Email
            password = request.POST.get('password')
            # Username / Email
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_writer == True:
                login(request, user)
                messages.success(request, "Welcome writer")
                return redirect('writer:writer-dashboard')
            if user is not None and user.is_writer == False:
                login(request, user)
                messages.success(request, "Welcome client")
                return redirect('client:client-dashboard')

    context = {
        'form': form,
    }
    return render(request, 'accounts/my-login.html', context)


# Logout User
@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('accounts:home')


@login_required(login_url='accounts:my-login')
def password_change(request):
    user = request.user
    form = UserChangePasswordForm(user)

    if request.method == 'POST':
        form = UserChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, form.user)
            return redirect('accounts:password-change-done')

    context = {
        'form': form,
    }
    return render(request, 'accounts/registration/password-change.html', context)


@login_required(login_url='accounts:my-login')
def password_change_done(request):
    messages.success(request, 'Your password has been changed successfully')
    return redirect('accounts:my-login')
