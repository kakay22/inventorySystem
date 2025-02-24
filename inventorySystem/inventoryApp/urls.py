from django.contrib import admin # type: ignore
from django.urls import path, include #type: ignore
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
	path("increase-stock/", views.increase_stock, name="increase_stock"),
    path("decrease-stock/", views.decrease_stock, name="decrease_stock"),
    path('categories/', views.categories, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
	path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
	path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
	path('logs/', views.logs, name='logs'),
	path('manage/', views.manage, name='manage'),
    path('product_users/', views.product_users, name='product_users'),
	path('add_product/', views.add_product, name='add_product'),
	path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
	path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
	path('add_user/', views.add_user, name='add_user'),
	path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
	path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
]
