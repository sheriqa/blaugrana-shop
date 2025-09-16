from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse #tugas3
from django.core import serializers #tugas3
from .models import Product
from .form import ProductForm


def show_main(request):
    context = {
        'shop_name': 'Blaugrana Shop',
        'owner': 'A. Sheriqa Dewina Ihsan [2406360722]',
        'class': 'PBP B',
        'products': Product.objects.all()  
    }
    return render(request, "main.html", context)

#tugas3 -- Serialisasi

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

#tombol add dn detail

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

