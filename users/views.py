from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from users.forms import UserLoginForm


def user_login(request):
    context = {}

    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid Login Details')
                return redirect('users:login')
            else:
                login(request, user)
                return HttpResponse('Logged in')

    context['form'] = form
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect('users:login')


#def user_register(request):
