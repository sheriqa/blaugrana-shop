from django.shortcuts import render
from .models import Product

def show_main(request):
    context = {
        'shop_name': 'Blaugrana Shop',
        'owner': 'A. Sheriqa Dewina Ihsan [2406360722]',
        'class': 'PBP B',
        'products': Product.objects.all()  
    }
    return render(request, "main.html", context)
