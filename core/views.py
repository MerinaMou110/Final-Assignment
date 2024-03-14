from django.shortcuts import render
from django.views.generic import TemplateView
from library.models import Book
from category.models import Category



def home(request, category_slug = None): 
    
    data = Book.objects.all() 
    if category_slug is not None: 

        category = Category.objects.get(slug = category_slug) 
        data = Book.objects.filter(category  = category) 
    categories = Category.objects.all() # sob category dekhabo
    return render(request, 'index.html', {'data' : data, 'category' : categories})