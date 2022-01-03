from django.contrib import admin
from .models import ProductModel, Product, ProductPurchasedModel,ApplyLoanPlan
admin.site.register(ProductPurchasedModel)
admin.site.register(Product)
admin.site.register(ApplyLoanPlan)
# Register your models here.
