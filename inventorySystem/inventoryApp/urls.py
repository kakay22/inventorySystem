from django.contrib import admin # type: ignore
from django.urls import path, include #type: ignore
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('categories/', views.categories, name='categories'),
	path('logs/', views.logs, name='logs'),
	path('manage/', views.manage, name='manage'),
    path('product_users/', views.product_users, name='product_users'),
	path('add_product/', views.add_product, name='add_product'),
	path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
	path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),

]
