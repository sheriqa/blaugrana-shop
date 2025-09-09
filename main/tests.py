from django.test import TestCase, Client
from .models import Product

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')  # cek root url
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_product_creation(self):
        product = Product.objects.create(
            name="Jersey Barca 24/25",
            price=1500000,
            description="Home kit musim baru",
            thumbnail="https://example.com/jersey.jpg",
            category="jersey",
            is_featured=True
        )
        self.assertEqual(product.name, "Jersey Barca 24/25")
        self.assertEqual(product.price, 1500000)
        self.assertTrue(product.is_featured)

    def test_product_default_values(self):
        product = Product.objects.create(
            name="Kaus Barca Training",
            price=350000,
            description="Kaus untuk latihan",
            thumbnail="https://example.com/kaus.jpg",
            category="training",
        )
        self.assertFalse(product.is_featured)
