from django.shortcuts import render
from .models import Product

def show_main(request):
    context = {
        'shop_name': 'Blaugrana Shop',
        'owner': 'Sheriqa',
        'class': 'PBP B',
        'products': Product.objects.all()  # ambil semua produk
    }
    return render(request, "main.html", context)
