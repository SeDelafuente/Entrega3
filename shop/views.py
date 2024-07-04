from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.http import JsonResponse
from django.db.models import Sum
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

def product_list(request):
    products = Product.objects.all()
    total_items = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_ordered=False).first()
        if order:
            total_items = OrderItem.objects.filter(order=order).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'shop/product_list.html', {'products': products, 'total_items': total_items})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if created:
            order_item.quantity = 1
        else:
            order_item.quantity += 1
        order_item.save()

        total_items = OrderItem.objects.filter(order=order).aggregate(Sum('quantity'))['quantity__sum']

        return JsonResponse({'message': 'Product added to cart successfully!', 'total_items': total_items})
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    items = OrderItem.objects.filter(order=order)
    total_cost = order.get_total_cost() if order else 0
    return render(request, 'shop/cart.html', {'items': items, 'total_cost': total_cost})

@login_required
def purchase(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if request.method == 'POST' and order:
        order.is_ordered = True
        order.save()
        return redirect('product_list')
    return render(request, 'shop/purchase.html', {'order': order})

@login_required
def cancel_order(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if request.method == 'POST' and order:
        order.delete()
        return redirect('product_list')
    return render(request, 'shop/cancel_order.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})
