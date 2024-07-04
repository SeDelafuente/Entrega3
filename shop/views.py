from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, created_at__isnull=True)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += 1
        order_item.save()
    items = OrderItem.objects.filter(order=order)
    return render(request, 'shop/cart.html', {'items': items})
