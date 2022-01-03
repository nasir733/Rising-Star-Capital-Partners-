from django.db import models
from django.forms import ModelForm
from users.models import CustomUser


class LoanApplicationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'business_name',
            'business_address',
            'ein_number',
            'bank_name',
            'bank_account_number',

            'bank_routing_number',
        ]
