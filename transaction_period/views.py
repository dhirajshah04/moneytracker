from django.contrib import messages
from django.shortcuts import render, redirect

from money.models import Account, Money
from transaction_period.forms import TransactionPeriodCreateForm, TransactionPeriodChangeForm, \
    CloseTransactionPeriodForm
from transaction_period.models import TransactionPeriod


def transaction_settings_home(request):
    context = {}
    return render(request, 'transaction_period/transaction_settings_home.html', context)


def transaction_period_list(request):
    context = {}

    transaction_periods = TransactionPeriod.objects.filter(is_active=True, user=request.user)
    context['transaction_periods'] = transaction_periods
    return render(request, 'transaction_period/transaction_period_list.htm', context)


def transaction_period_create(request):
    context = {}

    form = TransactionPeriodCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            transaction_period = form.save(commit=False)
            transaction_period.user = request.user
            transaction_period.save()
            messages.info(request, 'New Transaction Period Added')
            return redirect('transaction_period:transaction_period_list')

    context['form'] = form
    return render(request, 'transaction_period/transaction_period_add.htm', context)


def transaction_period_edit(request, pk):
    context = {}

    try:
        transaction_period = TransactionPeriod.objects.get(pk=pk, user=request.user)
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
    form.fields['transaction_period'].queryset = TransactionPeriod.objects.filter(is_active=False, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            for tp in TransactionPeriod.objects.filter(is_active=True, user=request.user):
                tp.is_active = False
                tp.save()

            transaction_period = form.cleaned_data['transaction_period']
            transaction_period.is_active = True
            transaction_period.save()

            messages.info(request, "Transaction changed successfully!")
            return redirect('transaction_period:transaction_period_list')

    context['form'] = form
    return render(request, 'transaction_period/transaction_period_change.html', context)


def close_transaction_period(request):
    context = {}
    money = Money.objects.filter(transaction_period__is_active=True,  user=request.user)

    form = CloseTransactionPeriodForm(request.POST or None)
    form.fields['name'].queryset = TransactionPeriod.objects.filter(is_active=False, user=request.user)

    if request.method == 'POST':
        if form.is_valid():

            # closing active transaction period and adding opening balance in new transaction period

            for m in money:
                new_m = Money()
                new_m.amount = m.amount
                new_m.account = m.account
                new_m.user = request.user
                new_m.transaction_period = form.cleaned_data['name']
                new_m.save()

            for atp in TransactionPeriod.objects.filter(is_active=True, user=request.user):
                atp.is_active = False
                atp.save()

            tp = form.cleaned_data['name']
            tp.is_active = True
            tp.save()

            return redirect('transaction_period:transaction_period_close')
    context['form'] = form
    context['money'] = money
    return render(request, 'transaction_period/transaction_period_close.html', context)
