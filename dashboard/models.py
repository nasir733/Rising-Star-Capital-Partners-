from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
# Create your models here.


class ProductModel(models.Model):
    class Meta:
        abstract = True

    MONTH = 'Month'
    YEAR = 'Year'
    ONE_TIME = 'One time'
    recurring_choices = (
        (1, ONE_TIME),
        (2, MONTH),
        (3, YEAR)
    )

    # Override this in child classes
    type = 'product'

    name = models.CharField(max_length=500, default='Product', null=True)

    
    price = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, validators=[MinValueValidator(0)])
    charge = models.DecimalField(
        max_digits=100, default=0, decimal_places=2, validators=[MinValueValidator(0)])
    recurring = models.IntegerField(
        choices=recurring_choices, default=1, null=True)

    # whitelabel_portal = models.ForeignKey(Subdomain, on_delete=models.CASCADE, null=True, blank=True)

    product_id = models.CharField(max_length=100, null=True, blank=True)
    price_id = models.CharField(max_length=100, null=True, blank=True)
    price_lookup = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(ProductModel):
    description = models.TextField(null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    link = models.URLField(blank=True, null=True)


class ProductPurchasedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payments_left = models.DecimalField(
        max_digits=100, default=0, decimal_places=2)
    amount_left = models.DecimalField(
        max_digits=100, default=0, decimal_places=2)
    username = models.CharField(blank=True, null=True, max_length=50)
    password = models.CharField(blank=True, null=True, max_length=50)
    link = models.URLField(blank=True, null=True)
    logged_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} {self.user}"


class ApplyLoanPlan(models.Model):
    name=models.CharField(blank=True, null=True, max_length=120)
    loan_type=models.CharField(blank=True, null=True, max_length=120)
    price = models.CharField(blank=True, null=True, max_length=120)
    subscription_stripe_id = models.CharField(max_length=150)
    origin_fee_stripe_id = models.CharField(max_length=150)
    origin_fee =models.CharField(blank=True, null=True, max_length=120)
    aproved_loan_amount =models.CharField(blank=True, null=True, max_length=120)
    duration = models.CharField(blank=True, null=True, max_length=120)
    def __str__(self):
        return "{} {}$ {}/months".format(self.name,self.price,self.duration)

