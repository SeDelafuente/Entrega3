from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
]
