from django import forms

from transaction_period.models import TransactionPeriod


class TransactionPeriodCreateForm(forms.ModelForm):

    class Meta:
        model = TransactionPeriod
        fields = {
            'name',
            'start_date',
            'end_date',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Period Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_date = super(TransactionPeriodCreateForm, self).clean()

        start_date = cleaned_date.get('start_date')
        end_date = cleaned_date.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('start_date', 'Start Date must be smaller than end date')
        return cleaned_date


class TransactionPeriodEditForm(forms.ModelForm):

    class Meta:
        model = TransactionPeriod
        fields = {
            'name',
            'start_date',
            'end_date',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Period Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_date = super(TransactionPeriodEditForm, self).clean()

        start_date = cleaned_date.get('start_date')
        end_date = cleaned_date.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('start_date', 'Start Date must be smaller than end date')
        return cleaned_date


class TransactionPeriodChangeForm(forms.Form):
    transaction_period = forms.ModelChoiceField(
        label='Transaction Periods',
        queryset=TransactionPeriod.objects.filter(is_active=False),
        empty_label='Select Transaction Period',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
