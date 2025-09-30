from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse #tugas3
from django.core import serializers #tugas3
from .models import Product
from .forms import ProductForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Tugas 4
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout 
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required #tugas 4


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # ambil query param
    category = request.GET.get("category", None)    

    # Filter produk
    if filter_type == "all":
        products = Product.objects.all()
    elif filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.filter(user=request.user)

    if category:
        products = products.filter(category=category)  

    # Menu kategori untuk navbar
    menu_items = [
        {'name': 'Jersey', 'slug': 'jersey'},
        {'name': 'Shoes', 'slug': 'shoes'},
        {'name': 'Accessories', 'slug': 'accessories'},
        {'name': 'Ball', 'slug': 'ball'},
        {'name': 'Others', 'slug': 'others'},
    ]

    context = {
        'shop_name': 'Blaugrana Shop',
        'owner': 'A. Sheriqa Dewina Ihsan [2406360722]',
        'class': 'PBP B',
        'products': products,
        'menu_items': menu_items,
        'filter_type': filter_type,  # <-- penting untuk template
        'last_login': request.COOKIES.get('last_login'),
    }
    return render(request, "main.html", context)



#======Tugas 3=======

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

@login_required(login_url='/login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
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

#======Tugas 4=======
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("main:show_main")
    else:
        form = RegisterForm() 
    return render(request, "register.html", {"form": form})
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

#======Tugas 5=======
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {
        'form': form
    }
    return render(request, "edit_product.html", context)
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))