from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse #tugas3
from django.core import serializers #tugas3
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Tugas 4
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout 
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required #tugas 4


@login_required(login_url='/login')
def show_main(request):
    context = {
        'shop_name': 'Blaugrana Shop',
        'owner': 'A. Sheriqa Dewina Ihsan [2406360722]',
        'class': 'PBP B',
        'products': Product.objects.all(),
        'last_login': request.COOKIES.get('last_login'),
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

#======Tugas 4=======
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)
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
