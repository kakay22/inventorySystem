from django.shortcuts import render, redirect
from .models import Category, Product, Log, RemovedProduct, ProductUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

# Create your views here.

@login_required
def dashboard(request):
	total_products = Product.objects.all().order_by('-created_at').count
	total_categories = Category.objects.all().order_by('-created_at').count
	total_users = ProductUser.objects.all().count
	logs = Log.objects.all().order_by('-created_at')[:5]
	return render(request, 'dashboard.html', {'total_products':total_products, 'total_categories':total_categories, 'total_users':total_users, 'logs':logs})

@login_required
def products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products':products})

@login_required
def categories(request):
    # Annotate each category with the count of related products
    categories = Category.objects.annotate(total_items=Count('product'))
    return render(request, 'category.html', {'categories': categories})

@login_required
def logs(request):
	# Fetch all logs ordered by their creation timestamp (most recent first)
	logs = Log.objects.all().order_by('-created_at')
	return render(request, 'logs.html', {'logs':logs})

@login_required
def manage(request):
	users = ProductUser.objects.all()
	products = Product.objects.all()
	categories = Category.objects.all()
	return render(request, 'manage.html', {'users':users, 'products':products, 'categories':categories})

@login_required
def product_users(request):
    users = ProductUser.objects.all()
    return render(request, 'product_users.html', {'users':users})

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_name = request.POST.get('category')
        stock = request.POST.get('stock')
        user_name = request.POST.get('user')

        # Check for empty fields
        if not (name and category_name and stock and user_name):
            messages.error(request, "All fields are required.")
            return redirect('add_product')

        # Check if category exists, create it if not
        category, created = Category.objects.get_or_create(name=category_name)

        # Check if user exists
        try:
            product_user = ProductUser.objects.get(name=user_name)
        except ProductUser.DoesNotExist:
            messages.error(request, "Selected user does not exist.")
            return redirect('add_product')

        # Create and save the product
        product = Product(
            name=name,
            category=category,
            stock=stock,
            user=product_user
        )
        product.save()

        # Success message
        messages.success(request, f"Product '{name}' added successfully.")
        return redirect('manage')

    # Fetch users to populate the dropdown
    users = ProductUser.objects.all()
    return render(request, 'add_product.html', {'users': users})
