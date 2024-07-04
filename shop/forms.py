from django import forms
from .models import OrderItem

class CartForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
