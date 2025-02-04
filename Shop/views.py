from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from django.db.models import Q

def register(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Taken')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('login')

def product_list(request):
    category = request.GET.get('category')
    query = request.GET.get('q', '')

    products = Products.objects.all().order_by('-created_at')

    if category:
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'products': [
                {
                    'name': product.name,
                    'description': product.description,
                    'price': str(product.price),
                    'image_url': product.image.url if product.image else '',
                    'store': product.store.by_user.username,
                    'category': product.get_category_display()
                } for product in page_obj
            ],
            'has_next': page_obj.has_next()
        }
        return JsonResponse(data)

    return render(request, 'products_list.html', {'products': page_obj, 'query': query})

def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Products, id=id)

    cart_item, created = CartModel.objects.get_or_create(by_user=user, by_product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

def view_cart(request):
    cart_items = CartModel.objects.filter(by_user=request.user)

    for item in cart_items:
        item.total_price = item.by_product.price * item.quantity

    total_amount = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'cart.html', context)

def delete_items_from_cart(request, id):
    user = request.user
    by_product = get_object_or_404(Products, id=id)
    
    cart_item = CartModel.objects.filter(by_user=user, by_product=by_product).first()
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')