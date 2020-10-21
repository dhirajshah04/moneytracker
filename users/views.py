from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def user_login(request):
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect('users:login')
