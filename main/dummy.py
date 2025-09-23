from main.models import Product
from django.contrib.auth.models import User

Product.objects.all().delete()

user1, created = User.objects.get_or_create(username='user1')
if created:
    user1.set_password('pass1234')
    user1.save()

user2, created = User.objects.get_or_create(username='user2')
if created:
    user2.set_password('pass1234')
    user2.save()

Product.objects.create(
    user=user1,
    name="FC Barcelona Jersey 2025",
    price=1000000,
    description="Official home jersey",
    thumbnail="thumbnails/jersey.jpg"
)
Product.objects.create(
    user=user1,
    name="Barcelona Scarf",
    price=250000,
    description="Winter scarf Barça edition",
    thumbnail="thumbnails/scarf.jpg"
)
Product.objects.create(
    user=user1,
    name="Barcelona Ball",
    price=350000,
    description="Official match ball",
    thumbnail="thumbnails/ball.jpg"
)


Product.objects.create(
    user=user2,
    name="FC Barcelona Keychain",
    price=95000,
    description="Official keychain",
    thumbnail="thumbnails/keychain.jpg"
)
Product.objects.create(
    user=user2,
    name="Barcelona Cap",
    price=150000,
    description="Summer cap Barça edition",
    thumbnail="thumbnails/cap.jpg"
)
Product.objects.create(
    user=user2,
    name="Barcelona Mug",
    price=120000,
    description="Coffee mug with Barça logo",
    thumbnail="thumbnails/mug.jpg"
)

print("Dummy data berhasil dibuat!")
