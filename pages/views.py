from django.shortcuts import render


def user_dashboard(request):
    context = {}
    return render(request, 'end_user/user_dashboard.html', context)
