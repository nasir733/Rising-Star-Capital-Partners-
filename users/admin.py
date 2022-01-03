from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']
    fieldsets = (
        (
            (('User'), {
                'fields': ('username', 'password', 'email', 'business_name', 'business_address', 'ein_number','loan_subscription_type','loan_origin_paid','loan_subscription_id','loan_subscription_added','loan_subscription_added_date')
            }),
            (('Payment'), {
                'fields': ('bank_name', 'bank_account_number', 'bank_routing_number', 'voided_check_or_direct_deposit_form', 'credit_line', 'cash_line_of_credit', 'total_line_of_credit',)
            }),
            (('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }),
        ))


admin.site.register(CustomUser, CustomUserAdmin)
