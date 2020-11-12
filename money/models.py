from django.db import models
from django.db.models import Sum
from model_utils import Choices

from transaction_period.models import TransactionPeriod
from users.models import User

ACCOUNT_TYPE = Choices(
    'Bank',
    'Digital Wallet',
    'Cash',
)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts_user')
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPE, default=ACCOUNT_TYPE.Bank)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.account_name

    class Meta:
        db_table = 'money_account'


class Money(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moneys_user')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='moneys_account')
    transaction_period = models.ForeignKey(TransactionPeriod, on_delete=models.CASCADE, related_name='moneys_transaction_period')
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        db_table = 'money_money'

    @staticmethod
    def get_total_amount_in_account(user):
        total_amount = Money.objects.filter(transaction_period__is_active=True, user=user).aggregate(total=Sum('amount'))
        return total_amount
