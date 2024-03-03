from django import forms
from django.core.exceptions import ValidationError

from .models import Balance, Expense, Payment, Transfer


class PaymentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].queryset = Balance.objects.filter(account=user)
        self.fields['expense'].queryset = Expense.objects.filter(account=user)

    class Meta:
        model = Payment
        fields = ['name', 'description', 'amount', 'balance', 'expense']

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        balance = cleaned_data.get('balance')
        payment_amount = cleaned_data.get('amount')
        if payment_amount > balance.amount:
            raise ValidationError('Payment amount should be less or equal balance amount!')
        return cleaned_data


class TransferForm(forms.ModelForm):
    def __init__(self, user, from_str, to_str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_balance'].queryset = Balance.objects.filter(
            account=user, currency=from_str)
        self.fields['to_balance'].queryset = Balance.objects.filter(account=user, currency=to_str)

    class Meta:
        model = Transfer
        fields = ['amount', 'from_balance', 'to_balance']

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        from_balance = cleaned_data.get('from_balance')
        amount = cleaned_data.get('amount')
        if amount > from_balance.amount:
            raise ValidationError('Transfer amount should be less or equal from balance amount!')
        return cleaned_data


class CurrencyChooseForm(forms.Form):
    from_currency = forms.MultipleChoiceField(choices=Balance.CURRENCY_CHOICES)
    to_currency = forms.MultipleChoiceField(choices=Balance.CURRENCY_CHOICES)
