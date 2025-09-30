from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<uuid:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('product/detail/<uuid:pk>/', views.product_detail, name="product_detail"),
    path('products/create/', views.create_product, name="create_product"),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<uuid:id>/edit', views.edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', views.delete_product, name='delete_product'),
]



