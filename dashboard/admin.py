from django.contrib import admin
from .models import ProductModel, Product, ProductPurchasedModel
admin.site.register(ProductPurchasedModel)
admin.site.register(Product)
# Register your models here.
