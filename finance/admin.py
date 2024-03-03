from django.contrib import admin

from finance.models import Balance, Expense, Payment, Transfer

admin.site.register(Balance)
admin.site.register(Expense)


def safe_delete_payments(_, request, queryset):
    for payment in queryset:
        payment.delete()


safe_delete_payments.short_description = 'Safe delete selected payments'


class PaymentAdmin(admin.ModelAdmin):
    actions = [safe_delete_payments, ]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transfer)
