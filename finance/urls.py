from django.urls import path
from .views import (
    BalanceCreateView, BalanceListView,
    BalanceDetailView, BalanceUpdateView, BalanceDeleteView,
    ExpenseListView, ExpenseCreateView,
    ExpenseDetailView, ExpenseUpdateView, ExpenseDeleteView,
    PaymentListView, PaymentCreateView,
    PaymentDetailView, PaymentUpdateView, PaymentDeleteView,
    TransferListView, TransferCreateView, TransferCurrencyChooser
)

urlpatterns = [
    path('balance/list/', BalanceListView.as_view(), name='balance_list'),
    path('balance/create/', BalanceCreateView.as_view(), name='balance_create'),
    path('balance/<int:pk>/', BalanceDetailView.as_view(), name='balance_detail'),
    path('balance/<int:pk>/update/', BalanceUpdateView.as_view(), name='balance_update'),
    path('balance/<int:pk>/delete/', BalanceDeleteView.as_view(), name='balance_delete'),

    path('expense/list/', ExpenseListView.as_view(), name='expense_list'),
    path('expense/create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),

    path('payment/list/', PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payment/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),

    path('transfer/list/', TransferListView.as_view(), name='transfer_list'),
    path('transfer/create/', TransferCurrencyChooser.as_view(), name='transfer_create'),
    path('transfer/create/<str:from>/<str:to>/', TransferCreateView.as_view(), name='transfer_create_from_to'),
]
