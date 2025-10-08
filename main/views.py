from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse #tugas3
from django.core import serializers #tugas3
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Tugas 4
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout 
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse 
from django.contrib.auth.decorators import login_required #tugas 4
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    category = request.GET.get("category", None)

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    if category:
        products = products.filter(category=category)

    context = {
        "shop_name": "Blaugrana Shop",
        "owner": "A. Sheriqa Dewina Ihsan [2406360722]",
        "class": "PBP B",
        "last_login": request.COOKIES.get('last_login'),
        "products": products,
    }

    return render(request, "main.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'user_id': product.id,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]
    return JsonResponse(data, safe=False)


def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    data = {
        'id': str(product.id),
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category': product.category,
        'thumbnail': product.thumbnail,
        'is_featured': product.is_featured,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'user_id': product.id,
        'user_username': product.user.username if product.user else None,
    }
    return JsonResponse(data)

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created! Please log in.")
            return redirect('main:login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect('main:show_main')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, f"Welcome back, {user.username}!")
            return response
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    messages.info(request, "You have been logged out successfully.")
    return response

@login_required(login_url='/login')
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='/login')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({
                'success': True,
                'message': 'Product added successfully!',
            })
        else:
            print(form.errors)  # 🔥 Tambahkan ini
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Product updated successfully!',
                'product': {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                    "category": product.category,
                    "thumbnail": str(product.thumbnail.url) if product.thumbnail else None,
                    "is_featured": product.is_featured,
                    "created_at": product.created_at.isoformat() if product.created_at else None,
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required(login_url='/login')
def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id, user=request.user)
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully!'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)