from django.db import models
from money.models import Account
from transaction_period.models import TransactionPeriod
from users.models import User


class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incomes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_users')
    transaction_period = models.ForeignKey(TransactionPeriod, on_delete=models.CASCADE, related_name='income_transaction_period')
    description = models.CharField(max_length=250)
    income_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.income_amount

    class Meta:
        db_table = 'income_expense_income'
