from django.db import models

# Create your models here.
from category.models import Category
from django.contrib.auth.models import User
from . constants import TRANSACTION_TYPE
from user_accounts.models import UserAccount


# Create your models here.
class Book(models.Model):
    category = models.ManyToManyField(Category) # ekta post multiple categorir moddhe thakte pare abar ekta categorir moddhe multiple post thakte pare
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13)
    publication_date = models.DateField()
    genre = models.CharField(max_length=50)
    availability_status = models.BooleanField(default=True)
    description= models.TextField()
    available_copies = models.PositiveIntegerField(default=0)  # Added a field for available copies
    borrowing_price= models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='Library/media/uploads/',blank=True,null=True)
    borrow_book = models.BooleanField(default=False)
    def __str__(self):
        return self.title 
    

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Comments by {self.name}"
    

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'transactions', on_delete = models.CASCADE) 
     # when each transaction involves one specific book.
    # This is the appropriate choice if each transaction is associated with exactly one book.
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
   
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    borrowing_date = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        ordering = ['timestamp']  #sort korbe timestamp onujayi
 


        
