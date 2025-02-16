from django.contrib import admin
from .models import Category, Product, Log, RemovedProduct, ProductUser
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Log)
admin.site.register(RemovedProduct)
admin.site.register(ProductUser)