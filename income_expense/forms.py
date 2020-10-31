from django import forms

from income_expense.models import Income
from money.models import Account


class IncomeForm(forms.ModelForm):

    account = forms.ModelChoiceField(
        label='Account',
        queryset=Account.objects.filter(is_deleted=False),
        empty_label='Select Account',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Income
        fields = {
            'account',
            'description',
            'income_amount',
        }

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'income_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }
