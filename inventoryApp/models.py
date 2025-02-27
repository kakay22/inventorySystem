from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductUser(models.Model):
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # Optional
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(ProductUser, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)  # Optional user
    # image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Log(models.Model):
    action = models.CharField(max_length=100)
    details = models.TextField()
    user = models.CharField(max_length=100, blank=True, null=True)
    product = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user.name} on {self.created_at}"

class RemovedProduct(models.Model):
    product_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    removed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    removed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
