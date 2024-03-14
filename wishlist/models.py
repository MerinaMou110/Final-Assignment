from django.db import models
from django.contrib.auth.models import User
from library.models import Book
# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
