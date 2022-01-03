from django.db import models
from django.contrib.auth.models import AbstractUser

from dashboard.models import ApplyLoanPlan
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=120, unique=True, blank=True, null=True)
    password = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    business_name = models.CharField(max_length=120, blank=True, null=True)
    business_address = models.CharField(max_length=120, blank=True, null=True)
    ein_number = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=120, blank=True, null=True)
    bank_account_number = models.CharField(
        max_length=120, blank=True, null=True)

    bank_routing_number = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, blank=True, null=True)
    voided_check_or_direct_deposit_form = models.FileField(
        blank=True, null=True)
    credit_line = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, blank=True, null=True)
    cash_line_of_credit = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, blank=True, null=True)
    total_line_of_credit = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, blank=True, null=True)

    loan_subscription_type = models.ForeignKey(
        ApplyLoanPlan, on_delete=models.CASCADE, blank=True, null=True)
    loan_subscription_id = models.CharField(
        max_length=250, blank=True, null=True)
    loan_origin_paid = models.BooleanField(
        default=False, blank=True, null=True)
    loan_subscription_added =models.BooleanField(
        default=False, blank=True, null=True)
    loan_subscription_added_date = models.DateTimeField(
        blank=True, null=True)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
