from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from django.db.models import Q
import stripe
from django.conf import settings
import json
from .forms import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

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
            return redirect('products')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

@login_required(login_url='login')
def user_logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
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

@login_required(login_url='login')
def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Products, id=id)

    cart_item, created = CartModel.objects.get_or_create(by_user=user, by_product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def product_detail_view(request, id):
    product = Products.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url='login')
def checkout_page(request, id):
    product = get_object_or_404(Products, id=id)
    user = request.user

    return render(request, 'checkout.html', {'product': product, 'user': user})

@login_required(login_url='login')
def checkout(request, id):
    product = get_object_or_404(Products, id=id)
    user = request.user

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number")
            shipping_address = data.get("shipping_address")

            if not phone_number or not shipping_address:
                return JsonResponse({"error": "Phone number and address are required"}, status=400)

            checkout = CheckoutModel.objects.create(
                by_user=user,
                total_amount=product.price,
                phone_number=phone_number,
                shipping_address=shipping_address
            )
            checkout.items.set([product])

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": product.name},
                        "unit_amount": int(product.price * 100),
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=request.build_absolute_uri(f"/payment_success/{checkout.id}/"),
                cancel_url=request.build_absolute_uri("/payment_failed/"),
            )

            checkout.payment_id = session.id
            checkout.save()

            return JsonResponse({"session_id": session.id})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return render(request, "checkout.html", {"product": product, "user": user})

@login_required(login_url='login')
def payment_success(request, id):
    checkout = get_object_or_404(CheckoutModel, id=id)

    if checkout.payment_status != "Paid":
        checkout.payment_status = "Paid"
        checkout.save()

        order = OrderModel.objects.create(
            by_user=checkout.by_user,
            total_amount=checkout.total_amount,
            phone_number=checkout.phone_number,
            shipping_address=checkout.shipping_address
        )
        order.items.set(checkout.items.all())

        tracking_id = order.tracking_id

        checkout.delete()

        return render(request, "payment_success.html", {"order": order, "tracking_id": tracking_id})

    return render(request, "payment_success.html", {"checkout": checkout, "tracking_id": None})

@login_required(login_url='login')
def payment_failed(request):
    return render(request, "payment_failed.html")

@login_required(login_url='login')
def track_order(request):
    tracking_id = request.GET.get("tracking_id")
    order = None

    if tracking_id:
        try:
            order = OrderModel.objects.get(tracking_id=tracking_id)
        except OrderModel.DoesNotExist:
            order = None

    return render(request, "track_order.html", {"order": order, "tracking_id": tracking_id})

@login_required(login_url='login')
def all_orders_of_user(request):
    user = request.user
    orders = OrderModel.objects.filter(by_user=user)
    return render(request, 'all_orders.html', context={'user': user, 'orders': orders})

@login_required(login_url='login')
def delete_order(request, order_id):
    order = get_object_or_404(OrderModel, id=order_id, by_user=request.user)

    if order.can_delete():
        order.delete()
        messages.success(request, "Order deleted successfully.")
    else:
        messages.error(request, "You can only delete pending orders.")

    return redirect('all_orders')

@login_required(login_url='login')
def add_review(request, order_id):
    order = get_object_or_404(OrderModel, id=order_id, by_user=request.user)

    if order.order_status != 'delivered':
        messages.error(request, "You can only review products after the order is delivered.")
        return redirect('all_orders')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')  
        product = get_object_or_404(Products, id=product_id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.order = order
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('all_orders')

    form = ReviewForm()
    products = order.items.all() 

    return render(request, 'add_review.html', {'form': form, 'products': products, 'order': order})

@login_required(login_url='login')
def product_detail_view(request, id):
    product = get_object_or_404(Products, id=id)
    reviews = ProductReview.objects.filter(product=product).order_by('-created_at')
    store = product.store
    context = {
        'product': product,
        'reviews': reviews,
        'store': store,
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url='login')
def create_store(request):
    if request.method == 'POST':
        user = request.user
        category = request.POST.get('category')
        image = request.FILES.get('image')
        unique_name = request.POST.get('unique_name')
        if Stores.objects.filter(unique_name=unique_name).exists():
            messages.error(request, 'Store Name Is Already Taken')
        else:
            Stores.objects.create(
                by_user=user,
                category=category,
                image=image,
                unique_name=unique_name
            )
            messages.success(request, 'Store Successfully Created')
            return redirect('products')
    return render(request, 'create_store.html')

@login_required(login_url='login')
def add_product(request):
    stores = Stores.objects.filter(by_user=request.user)

    if not stores:
        messages.error(request, "You don't have a store yet. Please create a store first.")
        return redirect("create_store")

    if request.method == "POST":
        store_id = request.POST.get("store")

        try:
            store = Stores.objects.get(id=store_id)
        except Stores.DoesNotExist:
            messages.error(request, "Invalid store selection.")
            return redirect("add_product")

        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        new_product = Products(
            store=store,
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )
        new_product.save()

        messages.success(request, "Product added successfully!")
        return redirect("product_list")

    return render(request, "add_product.html", {"stores": stores})

@login_required(login_url='login')
def store_products(request, store_id):
    store = get_object_or_404(Stores, id=store_id)

    if store.by_user != request.user:
        return redirect('home')

    products = Products.objects.filter(store=store)

    for product in products:
        total_sales = CartModel.objects.filter(by_product=product).aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0
        product.sales = total_sales

    total_revenue = sum(product.price * product.sales for product in products)

    return render(request, 'store_products.html', {
        'store': store,
        'products': products,
        'total_revenue': total_revenue
    })

@login_required(login_url='login')
def cart_checkout(request):
    user = request.user
    cart_items = CartModel.objects.filter(by_user=user)
    total_amount = sum(item.by_product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number")
            shipping_address = data.get("shipping_address")

            if not phone_number or not shipping_address:
                return JsonResponse({"error": "Phone number and address are required"}, status=400)

            checkout = CheckoutModel.objects.create(
                by_user=user,
                total_amount=total_amount,
                phone_number=phone_number,
                shipping_address=shipping_address
            )
            checkout.items.set([item.by_product for item in cart_items])

            line_items = []
            for item in cart_items:
                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.by_product.name
                        },
                        "unit_amount": int(item.by_product.price * 100),
                    },
                    "quantity": item.quantity,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=request.build_absolute_uri(f"/payment_success/{checkout.id}/"),
                cancel_url=request.build_absolute_uri("/payment_failed/"),
            )

            checkout.payment_id = session.id
            checkout.save()

            return JsonResponse({"session_id": session.id})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return render(request, "cart_checkout.html", {"cart_items": cart_items, "total_amount": total_amount, "user": user})
