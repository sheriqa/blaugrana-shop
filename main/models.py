import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('ball', 'Ball'),
        ('others', 'Others'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    thumbnail = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Rp{self.price}"

    @property
    def is_available(self):
        """Cek apakah produk masih ada stoknya"""
        return self.stock > 0

    def reduce_stock(self, qty=1):
        """Kurangi stok produk ketika dibeli"""
        if self.stock >= qty:
            self.stock -= qty
            self.save()


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity
