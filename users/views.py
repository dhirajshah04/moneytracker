from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from users.forms import UserLoginForm,UserRegisterForm


def user_login(request):
    next = request.GET.get('next', None)
    if request.user.is_authenticated:
        return HttpResponse('already logged in')

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
                if next:
                    return redirect(next)
                return HttpResponse('Logged in')

    context['form'] = form
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect('users:login')


def user_register(request):
    context = {}

    form = UserRegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            messages.info(request, 'User Created, please login')
            return redirect('users:login')

    context['form'] = form
    return render(request, 'users/user_register.html', context)
