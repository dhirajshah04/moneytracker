from django.db import models
from model_utils import Choices

ACCOUNT_TYPE = Choices(
    'Bank',
    'Digital Wallet',
    'Cash',
)


class Account(models.Model):
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPE, default=ACCOUNT_TYPE.Bank)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.account_name

    class Meta:
        db_table = 'money_account'


class Money(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='moneys')
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount

    class Meta:
        db_table = 'money_money'
