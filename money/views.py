from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect

from income_expense.models import Income
from money.forms import AccountCreateForm, AccountEditForm, AddMoneyForm
from money.models import Account, Money
from transaction_period.models import TransactionPeriod


def account_list(request):
    context = {}

    accounts_list = Account.objects.filter(is_deleted=False, user=request.user)
    money = Money.objects.filter(user=request.user).aggregate(total=Sum('amount'))
    context['account_list'] = accounts_list
    context['money'] = money
    return render(request, 'money/list_account.html', context)


def add_account(request):
    context = {}

    form = AccountCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            messages.info(request, 'New Account Created')
            return redirect('money:add_account')

    context['form'] = form
    return render(request, 'money/add_account.html', context)


def edit_account(request, pk):
    context = {}

    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        messages.error(request, 'Account Does not Exist')
        return redirect('money:add_account')

    form = AccountEditForm(request.POST or None, instance=account)

    if request.method == 'POST':
        if form.is_valid():
            account = form.save()
            account.save()

            messages.info(request, 'Account Updated')
            return redirect('money:add_account')

    context['form'] = form
    return render(request, 'money/edit_account.html', context)


# delete account

def add_money(request):
    context = {}

    try:
        active_transaction_period = TransactionPeriod.objects.get(is_active=True, user=request.user)
    except TransactionPeriod.DoesNotExist:
        messages.error(request, 'Active Transaction Period Not found, please activate or create at least one')
        return redirect('transaction_period:transaction_period_list')

    form = AddMoneyForm(request.POST or None)

    # Filters the account foreign key based on user logged in
    form.fields["account"].queryset = Account.objects.filter(is_deleted=False, user=request.user)

    if request.method == 'POST':
        if form.is_valid():
            money = form.save(commit=False)
            money.user = request.user
            money.transaction_period = active_transaction_period

            income = Income()
            income.account = money.account
            income.income_amount = money.amount
            income.user = request.user
            income.transaction_period = active_transaction_period
            income.description = 'First or original balance in {}'.format(money.account.account_name)
            income.save()

            money.save()

            messages.info(request, 'Money Added')
            return redirect('money:add_account')

    context['form'] = form
    return render(request, 'money/add_money.html', context)

