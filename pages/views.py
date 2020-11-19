from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse

from income_expense.models import Income, Expense
from users.decorators import login_required


@login_required
def bar_report_home(request):
    return render(request, 'bar_report_home.html')


@login_required
def income_expense_bar_chart(request):
    labels = []
    income_data = []
    expense_data = []

    income_queryset = Income.objects.filter(user=request.user, transaction_period__is_active=True).values(
                                    'transaction_period__name').annotate(total_income=Sum('income_amount'))
    for income in income_queryset:
        labels.append(income['transaction_period__name'])
        income_data.append(income['total_income'])

    expense_queryset = Expense.objects.filter(user=request.user, transaction_period__is_active=True).values(
        'transaction_period__name').annotate(total_expense=Sum('expense_amount'))

    for expense in expense_queryset:
        expense_data.append(expense['total_expense'])

    return JsonResponse(data={
        'labels': labels,
        'income_data': income_data,
        'expense_data': expense_data,
    })
