from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import AdminProfile, CustomerProfile
from .admin_forms import CustomerProfileAdminForm, AdminProfileAdminForm

admin.site.register(get_user_model())


class CustomerProfileAdmin(admin.ModelAdmin):
    form = CustomerProfileAdminForm


class AdminProfileAdmin(admin.ModelAdmin):
    form = AdminProfileAdminForm


admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)
