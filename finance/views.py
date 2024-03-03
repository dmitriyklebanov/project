from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)

from finance.forms import PaymentForm, TransferForm, CurrencyChooseForm
from finance.models import Balance, Expense, Payment, Transfer

from .currency import get_currency_rate

import logging


logger = logging.getLogger('django')


class UsersCreateView(LoginRequiredMixin, CreateView):
    template_name = 'finance/form.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name.capitalize()
        return res


class UsersListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)


class OrderedUsersListView(UsersListView):
    def get_queryset(self):
        return super().get_queryset().order_by('-datetime')


class UsersDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        obj = super().get_object()
        if obj.account != self.request.user:
            raise PermissionDenied
        return obj


class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'finance/form.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().account == self.request.user

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name.capitalize()
        return res


class UsersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'finance/confirm_delete.html'

    def test_func(self):
        return self.get_object().account == self.request.user

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name
        res['detail_url'] = self.model._meta.model_name + '_detail'
        return res


class BalanceListView(UsersListView):
    model = Balance


class BalanceCreateView(UsersCreateView):
    model = Balance
    fields = ['name', 'amount', 'currency']


class BalanceDetailView(UsersDetailView):
    model = Balance

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['payment_list'] = Payment.objects.filter(balance=res['object']).order_by('-datetime')
        return res


class BalanceUpdateView(UsersUpdateView):
    model = Balance
    fields = ['name', 'amount']


class BalanceDeleteView(UsersDeleteView):
    model = Balance
    success_url = reverse_lazy('balance_list')


class ExpenseListView(UsersListView):
    model = Expense


class ExpenseCreateView(UsersCreateView):
    model = Expense
    fields = ['name']


class ExpenseDetailView(UsersDetailView):
    model = Expense

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['payment_list'] = Payment.objects.filter(expense=res['object']).order_by('-datetime')
        return res


class ExpenseUpdateView(UsersUpdateView):
    model = Expense
    fields = ['name']


class ExpenseDeleteView(UsersDeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')


class PaymentListView(OrderedUsersListView):
    model = Payment


class PaymentCreateView(UsersCreateView):
    model = Payment
    form_class = PaymentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.balance.amount -= form.instance.amount
        form.instance.balance.save()
        return super().form_valid(form)


class PaymentDetailView(UsersDetailView):
    model = Payment


class PaymentUpdateView(UsersUpdateView):
    model = Payment
    fields = ['name', 'description', 'expense']


class PaymentDeleteView(UsersDeleteView):
    model = Payment
    success_url = reverse_lazy('payment_list')


class TransferListView(OrderedUsersListView):
    model = Transfer


class TransferCreateView(UsersCreateView):
    model = Transfer
    form_class = TransferForm
    success_url = reverse_lazy('transfer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'from_str': self.kwargs['from']})
        kwargs.update({'to_str': self.kwargs['to']})
        return kwargs

    def get(self, request, *args, **kwargs):
        from_str = kwargs.get('from')
        to_str = kwargs.get('to')
        if from_str != to_str:
            coef = get_currency_rate(from_str, to_str)
            msg = f'Exchange rate from {kwargs.get("from")} to {kwargs.get("to")} is {coef}!'
            messages.warning(request, msg)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        from_balance = form.instance.from_balance
        to_balance = form.instance.to_balance
        form.instance.coef = get_currency_rate(from_balance.currency, to_balance.currency)
        from_balance.amount -= form.instance.amount * form.instance.coef
        from_balance.save()
        to_balance.amount += form.instance.amount * form.instance.coef
        to_balance.save()
        return super().form_valid(form)


class TransferCurrencyChooser(FormView):
    form_class = CurrencyChooseForm
    template_name = 'finance/form.html'

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = 'Choose currencies'
        return res

    def form_valid(self, form):
        return redirect(
            'transfer_create_from_to',
            form.data['from_currency'],
            form.data['to_currency']
        )
