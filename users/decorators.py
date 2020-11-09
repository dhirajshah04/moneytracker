from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from moneytracker import settings


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('money:list_account')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    login_url = settings.LOGIN_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def super_admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superadmin():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def end_user_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_enduser():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
