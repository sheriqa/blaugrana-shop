from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
app_name = 'main'
def debug_urls(request):
    from django.urls import get_resolver
    url_list = []
    resolver = get_resolver()
    
    def extract_urls(pattern_list, prefix=''):
        for pattern in pattern_list:
            if hasattr(pattern, 'url_patterns'):
               
                extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                url_list.append({
                    'pattern': prefix + str(pattern.pattern),
                    'name': getattr(pattern, 'name', 'No name')
                })
    
    extract_urls(resolver.url_patterns)
    return JsonResponse(url_list, safe=False)


urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<uuid:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('product/detail/<uuid:pk>/', views.product_detail, name="product_detail"),
    path('products/create/', views.create_product, name="create_product"),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<uuid:id>/edit', views.edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', views.delete_product, name='delete_product'),
    path('debug-urls/', debug_urls),
]




