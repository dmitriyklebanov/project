from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

import pytest

from finance.models import Balance, Expense, Payment


USER_PASSWORD = '1234'
BALANCE_AMOUNT = 10000


@pytest.fixture()
def create_balances():
    user1 = User.objects.create(username='tmp1')
    user1.set_password(USER_PASSWORD)
    user1.save()
    user2 = User.objects.create(username='tmp2')
    user2.set_password(USER_PASSWORD)
    user2.save()
    balance1 = Balance.objects.create(account=user1, name='balance1', amount=BALANCE_AMOUNT)
    balance2 = Balance.objects.create(account=user2, name='balance2', amount=BALANCE_AMOUNT)
    return Client(), user1, user2, balance1, balance2


def login(client, user):
    client.login(username=user.username, password=USER_PASSWORD)


@pytest.mark.django_db
class TestBalanceViews:
    def test_balance_list_view(self, create_balances):
        url = reverse('balance_list')
        client, user, _, _, _ = create_balances
        login(client, user)

        response = client.get(url)
        assert response.status_code == 200

    def test_balance_list_view_content(self, create_balances):
        url = reverse('balance_list')
        client, user, _, _, _ = create_balances
        login(client, user)

        response = client.get(url)
        assert response.status_code == 200
        assert 'balance1' in str(response.content)
        assert 'balance2' not in str(response.content)

    def test_balance_create_view_content(self, create_balances):
        url = reverse('balance_create')
        client, user, _, _, _ = create_balances
        login(client, user)

        balance = {
            'amount': 42,
            'name': 'test',
            'currency': 'USD',
        }

        response = client.post(url, balance)
        assert response.status_code == 302
        assert Balance.objects.filter(name='test').count() == 1

    @pytest.mark.parametrize("balance, status_code", [
        (1, 200),
        (2, 403)])
    def test_balance_detail_view(self, create_balances, balance, status_code):
        client, user, _, _, _ = create_balances
        login(client, user)

        balance = create_balances[2 + balance]
        url = reverse('balance_detail', kwargs={'pk': balance.id})
        response = client.get(url)
        assert response.status_code == status_code

    @pytest.mark.parametrize("amount, status_code", [
        (324234, 200),
        (42, 200)])
    def test_balance_update_view(self, create_balances, amount, status_code):
        client, user, _, balance, _ = create_balances
        login(client, user)

        url = reverse('balance_update', kwargs={'pk': balance.id})
        response = client.post(url, {'amount': amount})
        assert response.status_code == status_code
        balance = Balance.objects.get(name='balance1')
        if status_code == 302:
            assert balance.amount == amount
        else:
            assert balance.amount == BALANCE_AMOUNT


@pytest.fixture()
def create_balances_and_expenses():
    user1 = User.objects.create(username='tmp1')
    user1.set_password(USER_PASSWORD)
    user1.save()
    user2 = User.objects.create(username='tmp2')
    user2.set_password(USER_PASSWORD)
    user2.save()

    balance1 = Balance.objects.create(account=user1, name='balance1', amount=BALANCE_AMOUNT)
    balance2 = Balance.objects.create(account=user2, name='balance2', amount=BALANCE_AMOUNT)

    expense1 = Expense.objects.create(account=user1, name='expense1')
    expense2 = Expense.objects.create(account=user2, name='expense2')

    return Client(), user1, user2, balance1, balance2, expense1, expense2


@pytest.mark.django_db
class TestPaymentViews:
    @pytest.mark.parametrize("amount, status_code", [
        (10000, 302),
        (20000, 200)])
    def test_payment_create_view(self, create_balances_and_expenses, amount, status_code):
        client, user, _, balance, _, expense, _ = create_balances_and_expenses
        login(client, user)
        url = reverse('payment_create')
        payment = {
            'amount': amount,
            'title': 'test',
            'balance': balance.pk,
            'expense': expense.pk,
        }

        response = client.post(url, payment)
        assert response.status_code == status_code
        balance = Balance.objects.get(name='balance1')
        if amount <= BALANCE_AMOUNT:
            assert balance.amount == pytest.approx(float(BALANCE_AMOUNT - amount))
            assert Payment.objects.filter(title='test').count() == 1
        else:
            assert balance.amount == pytest.approx(BALANCE_AMOUNT)
