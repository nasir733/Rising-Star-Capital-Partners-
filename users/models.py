from django.db import models
from django.contrib.auth.models import AbstractUser
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

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
