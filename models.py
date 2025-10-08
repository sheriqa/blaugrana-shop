import uuid
from django.db import models
from django.contrib.auth.models import User

class Book(models.Models):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=255)

class Author(models.Models):
    bio=models.TextField()
    books = models.ManyToManyField(Book)
    user = models.OneToOneField(User, on_delete=models.CASCADE)