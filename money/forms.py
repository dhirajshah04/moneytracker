from django import forms
from money.models import Account, Money


class AccountCreateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = {
            'account_name',
            'account_type',
        }

        widgets = {
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Name'}),
            'account_type' : forms.Select(attrs={'class': 'form-control'}),
        }


class AccountEditForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = {
            'account_name',
            'account_type',
        }

        widgets = {
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Name'}),
            'account_type' : forms.Select(attrs={'class': 'form-control'}),
        }


class AddMoneyForm(forms.ModelForm):

    account = forms.ModelChoiceField(
        label='Account',
        queryset=Account.objects.filter(is_deleted=False),
        empty_label='Select Account Type',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Money
        fields = {
            'account',
            'amount',
        }

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }
