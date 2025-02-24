from django.shortcuts import render, redirect
from .models import Category, Product, Log, RemovedProduct, ProductUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .utils import record_log  

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
    users = ProductUser.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products.html', {'products':products, 'users':users, 'categories':categories})

def increase_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 0))

        product = get_object_or_404(Product, id=product_id)

        if quantity > 0:
            product.stock += quantity
            product.save()
            messages.success(request, f"Successfully added {quantity} to {product.name}'s stock.")
        else:
            messages.error(request, "Invalid quantity entered.")

    return redirect("manage")  # Change to your actual product listing URL

def decrease_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 0))

        product = get_object_or_404(Product, id=product_id)

        if quantity > 0 and product.stock >= quantity:
            product.stock -= quantity
            product.save()
            messages.success(request, f"Successfully removed {quantity} from {product.name}'s stock.")
        else:
            messages.error(request, "Invalid quantity or insufficient stock.")

    return redirect("manage")  # Change to your actual product listing URL

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def edit_product(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        stock = request.POST.get('stock')

        category_instance = get_object_or_404(Category, name=category)

        # Find the product and update its fields
        product = get_object_or_404(Product, id=pk)
        product.name = name
        product.category = category_instance
        product.stock = stock
        product.save()

        # Record the log
        product_user = product.user.name
        user_instance = ProductUser.objects.get(name=product_user)
        action = "edited product"
        details = f"Product '{name}' has ben edited"
        record_log(action, details, user_instance, product)

        # Return a success response
        # return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
        return redirect('products')
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})


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
    users = ProductUser.objects.annotate(product_count=Count("products"))  # Count products per user
    return render(request, 'product_users.html', {'users': users})

def edit_user(request, pk):
    user = get_object_or_404(ProductUser, pk=pk)

    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if username and email:
            user.name = username
            user.email = email
            user.phone = phone
            user.save()

            return redirect('product_users')

def delete_user(request, pk):
    user = get_object_or_404(ProductUser, pk=pk)
    user.delete()
    return redirect('product_users')

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

        user_instance = ProductUser.objects.get(name=user_name)
        # Record the log
        action = "Added Product"
        details = f"Product '{name}' added with stock {stock} in category '{category}'."
        record_log(action, details, user_instance, product)

        # Success message
        messages.success(request, f"Product '{name}' added successfully.")
        return redirect('manage')

    # Fetch users to populate the dropdown
    users = ProductUser.objects.all()
    return render(request, 'add_product.html', {'users': users})


def delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)

        # Record the log
        product_user = product.user.name
        user_instance = ProductUser.objects.get(name=product_user)
        action = "Deleted product"
        details = f"Product '{product.name}' has ben deleted"
        record_log(action, details, user_instance, product)
        
        product.delete()

        return redirect('products')


def add_category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        category_description = request.POST.get('category_description')

        Category.objects.create(
            name=category,
            description=category_description
        )

        # Record the log
        product_user = 'N/A'
        product = 'N/A'
        user_instance = 'N/A'
        action = "New category added"
        details = f"Category '{category}' has ben added"
        record_log(action, details, user_instance, product)

        return redirect('categories')

def edit_category(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('category_description')

        if category_name and description:
            category.name = category_name
            category.description = description

            # Record the log
            product_user = 'N/A'
            product = 'N/A'
            user_instance = 'N/A'
            action = f"category updated"
            details = f"Category '{category}' has ben updated"
            record_log(action, details, user_instance, product)

            category.save()

            return redirect('categories')

def delete_category(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)

        # Record the log
        product_user = 'N/A'
        product = 'N/A'
        user_instance = 'N/A'
        action = f"category deleted"
        details = f"Category '{category}' has ben deleted"
        record_log(action, details, user_instance, product)        

        category.delete()
        return redirect('categories')


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            # Create user
            new_user = ProductUser.objects.create(
                name=username,
                email=email
            )

            # Record the log
            action = "User Added"
            details = f"User '{new_user.name}' with email '{new_user.email}' has been added."
            user_instance = new_user  # Logging the actual user instance
            product = 'N/A'  # Update if necessary

            record_log(action, details, user_instance, product)

        return redirect('product_users')