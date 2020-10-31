from django.contrib import messages
from django.shortcuts import render, redirect
from income_expense.forms import IncomeForm
from income_expense.models import Income
from money.models import Money


def income_add(request):
    context = {}

    form = IncomeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():

            income_amt = form.save(commit=False)
            income_amt.user = request.user

            # Updating the Money in accounts section too while adding incomes

            account_id = income_amt.account.id  # Takes account ID from income form, select account filed

            try:
                account_money = Money.objects.get(account_id=account_id)  # Filters the money model related to the accound_id
                add_money = form.cleaned_data.get('income_amount')  # Gets income amount from income form
                account_money.amount = account_money.amount + add_money  # Adds income amount to existing amount in account
                account_money.save()
            except Money.DoesNotExist:
                add_money = form.cleaned_data.get('income_amount')
                new_money = Money()
                new_money.account = income_amt.account
                new_money.amount = add_money
                new_money.user = request.user
                new_money.save()

            income_amt.save()

            messages.info(request, 'Income Added')
            return redirect('income_expense:income_add')

    context['form'] = form
    return  render(request, 'income_expense/income_add.html', context)


def income_list(request):
    context = {}

    income = Income.objects.filter(user=request.user)
    context['income'] = income
    return render(request, 'income_expense/income_list.html', context)
