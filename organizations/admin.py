from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Domain, Organization


class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 1


@admin.register(Organization)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = (
        "schema_name",
        "name",)
    inlines = [DomainInline]