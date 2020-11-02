from django.contrib import messages
from django.shortcuts import render, redirect

from transaction_period.forms import TransactionPeriodCreateForm, TransactionPeriodChangeForm
from transaction_period.models import TransactionPeriod


def transaction_period_list(request):
    context = {}

    transaction_periods = TransactionPeriod.objects.filter(is_active=True)
    context['transaction_periods'] = transaction_periods
    return render(request, 'transaction_period/transaction_period_list.htm', context)


def transaction_period_create(request):
    context = {}

    form = TransactionPeriodCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            transaction_period = form.save(commit=False)
            transaction_period.save()
            messages.info(request, 'New Transaction Period Added')
            return redirect('transaction_period:transaction_period_list')

    context['form'] = form
    return render(request, 'transaction_period/transaction_period_add.htm', context)


def transaction_period_edit(request, pk):
    context = {}

    try:
        transaction_period = TransactionPeriod.objects.get(pk=pk)
    except TransactionPeriod.DoesNotExist:
        messages.error(request, 'Transaction Period Does Not Exist!')
        return redirect('transaction_period:transaction_period_list')

    form = TransactionPeriodCreateForm(request.POST or None, instance=transaction_period)

    if request.method == 'POST':
        if form.is_valid():
            transaction_period = form.save(commit=False)
            transaction_period.save()
            messages.info(request, 'Transaction Period Updated')
            return redirect('transaction_period:transaction_period_list')

    context['form'] = form
    return render(request, 'transaction_period/transaction_period_edit.htm', context)


def transaction_period_change(request):
    context = {}

    form = TransactionPeriodChangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            for tp in TransactionPeriod.objects.filter(is_active=True):
                tp.is_active = False
                tp.save()

            transaction_period = form.cleaned_data['transaction_period']
            transaction_period.is_active = True
            transaction_period.save()

            messages.info(request, "Transaction changed successfully!")
            return redirect('transaction_period:transaction_period_list')

    context['form'] = form
    return render(request, 'transaction_period/transaction_period_change.html', context)
