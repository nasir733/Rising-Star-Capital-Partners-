from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password',
                  'business_name', 'business_address')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password',
                  'business_name', 'business_address')


class UpperField(forms.CharField):
    def to_python(self, value):
        return value.upper()


class CustomUpdateUserForm(forms.ModelForm):
    bank_account_number = UpperField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'bank_account_number', 'bank_name', 'business_name', 'business_address', "ein_number",
                  'bank_routing_number', 'voided_check_or_direct_deposit_form', 'total_line_of_credit']
