from django import template
from money.models import Account, Money


register = template.Library()


@register.simple_tag
def get_money_active_transaction_account(account_id):
    account = Account.objects.get(id=account_id)
    money = Money.objects.get(transaction_period__is_active=True, account=account, transaction_period__is_closed=False)
    return str(money)


@register.simple_tag
def get_money_close_transaction_account(account_id):
    account = Account.objects.get(id=account_id)
    money = Money.objects.get(transaction_period__is_active=True, account=account, transaction_period__is_closed=True)
    return str(money)
