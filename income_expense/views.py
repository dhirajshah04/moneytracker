from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from income_expense.forms import IncomeForm, ExpenseForm
from income_expense.models import Income, Expense
from money.models import Money, Account
from moneytracker.utils import render_pdf
from transaction_period.models import TransactionPeriod


def income_add(request):
    context = {}

    try:
        active_transaction_period = TransactionPeriod.objects.get(is_active=True, user=request.user)
    except TransactionPeriod.DoesNotExist:
        messages.error(request, 'Active Transaction Period Not found, please activate at least one')
        return redirect('transaction_period:transaction_period_list')

    form = IncomeForm(request.POST or None)

    # Filters the account foreign key based on user logged in
    form.fields["account"].queryset = Account.objects.filter(is_deleted=False, user=request.user)

    if request.method == 'POST':
        if form.is_valid():

            income_amt = form.save(commit=False)
            income_amt.user = request.user
            income_amt.transaction_period = active_transaction_period

            # Updating the Money in accounts section too while adding incomes

            account_id = income_amt.account.id  # Takes account ID from income form, select account filed

            try:
                account_money = Money.objects.get(account_id=account_id, transaction_period__is_active=True)  # Filters the money model related to the accound_id
                add_money = form.cleaned_data.get('income_amount')  # Gets income amount from income form
                account_money.amount = account_money.amount + add_money  # Adds income amount to existing amount in account
                account_money.save()
            except Money.DoesNotExist:
                add_money = form.cleaned_data.get('income_amount')
                new_money = Money()
                new_money.account = income_amt.account
                new_money.amount = add_money
                new_money.user = request.user
                new_money.transaction_period = active_transaction_period
                new_money.save()

            income_amt.save()

            messages.info(request, 'Income Added')
            return redirect('income_expense:income_add')

    context['form'] = form
    return render(request, 'income_expense/income_add.html', context)


def income_list(request):
    context = {}

    pdf_report = request.GET.get('pdf_report', '')

    income = Income.objects.filter(user=request.user, transaction_period__is_active=True)
    total_income = income.aggregate(Sum('income_amount'))
    transaction_period = TransactionPeriod.get_active_transaction_period(request)
    context['income'] = income
    context['total_income'] = total_income
    context['transaction_period'] = transaction_period

    if pdf_report == 'pdf':
        return render_pdf('income_expense/income_report_pdf.html', context,
                          filename='income_report_{}.pdf'.format(transaction_period))

    return render(request, 'income_expense/income_list.html', context)


def expense_list(request):
    context = {}

    pdf_report = request.GET.get('pdf_report', '')

    expense = Expense.objects.filter(user=request.user, transaction_period__is_active=True)
    total_expense = expense.aggregate(Sum('expense_amount'))
    transaction_period = TransactionPeriod.get_active_transaction_period(request)
    context['expense'] = expense
    context['total_expense'] = total_expense
    context['transaction_period'] = transaction_period

    if pdf_report == 'pdf':
        return render_pdf('income_expense/expense_report_pdf.html', context,
                          filename='expense_report_{}.pdf'.format(transaction_period))

    return render(request, 'income_expense/expense_list.html', context)


def expense_add(request):
    context = {}

    try:
        active_transaction_period = TransactionPeriod.objects.get(is_active=True, user=request.user)
    except TransactionPeriod.DoesNotExist:
        messages.error(request, 'Active Transaction Period Not found, please activate at least one')
        return redirect('transaction_period:transaction_period_list')

    form = ExpenseForm(request.POST or None)

    # Filters the account foreign key based on user logged in
    form.fields["account"].queryset = Account.objects.filter(is_deleted=False, user=request.user)

    if request.method == 'POST':
        if form.is_valid():

            expense_amt = form.save(commit=False)
            expense_amt.user = request.user
            expense_amt.transaction_period = active_transaction_period

            # Updating the Money in accounts section too while adding expense

            account_id = expense_amt.account.id  # Takes account ID from income form, select account filed

            try:
                account_money = Money.objects.get(account_id=account_id, transaction_period__is_active=True)  # Filters the money model related to the accound_id
                spent_money = form.cleaned_data.get('expense_amount')  # Gets income amount from income form
                account_money.amount = account_money.amount - spent_money  # Adds income amount to existing amount in account
                account_money.save()
            except Money.DoesNotExist:
                messages.warning(request, 'No money in the account selected to spend')
                return redirect('money:list_account')
                # spent_money = form.cleaned_data.get('expense_amount')
                # new_money = Money()
                # new_money.account = expense_amt.account
                # new_money.amount = spent_money
                # new_money.user = request.user
                # new_money.transaction_period = active_transaction_period
                # new_money.save()

            expense_amt.save()

            messages.info(request, 'Expense Added')
            return redirect('income_expense:expense_add')

    context['form'] = form
    return render(request, 'income_expense/expense_add.html', context)

