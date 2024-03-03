from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Balance(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('EUR', 'Euro'),
        ('RUB', 'Russian Ruble'),
    ]

    MAX_VALUE = 999999999999999

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField(validators=[MaxValueValidator(MAX_VALUE), MinValueValidator(0)])
    currency = models.CharField(max_length=5, default='USD', choices=CURRENCY_CHOICES)

    def __str__(self):
        return f'{self.account.username}_{self.name}'

    def get_absolute_url(self):
        return reverse('balance_detail', kwargs={'pk': self.pk})


class Expense(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.account.username}_{self.name}'

    def get_absolute_url(self):
        return reverse('expense_detail', kwargs={'pk': self.pk})

    def get_default(self):
        return Expense.objects.get_or_create(account=self.account, name='other')[0]

    def delete(self):
        payments = Payment.objects.filter(expense=self)
        for payment in payments:
            payment.expense = self.get_default()
            payment.save()

        super().delete()


class Payment(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(validators=[
        MaxValueValidator(Balance.MAX_VALUE), MinValueValidator(0)])
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.account.username}_{self.pk}'

    def delete(self):
        self.balance.amount = min(Balance.MAX_VALUE, self.balance.amount + self.amount)
        self.balance.save()
        super().delete()

    def get_absolute_url(self):
        return reverse('payment_detail', kwargs={'pk': self.pk})


class Transfer(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    datetime = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(validators=[
        MaxValueValidator(Balance.MAX_VALUE), MinValueValidator(0)])
    coef = models.FloatField(validators=[
        MaxValueValidator(Balance.MAX_VALUE), MinValueValidator(0)])
    from_balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='from_balance')
    to_balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='to_balance')

    def __str__(self):
        return f'{self.account.username}_{self.pk}'
