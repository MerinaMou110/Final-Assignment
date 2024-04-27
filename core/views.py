from django.shortcuts import render
from django.views.generic import TemplateView
from library.models import Book
from category.models import Category




def home(request, category_slug=None): 
    query = request.GET.get('keyword')  # Get the search query from the request

    # Filter books by category if a category slug is provided
    if category_slug is not None: 
        category = Category.objects.get(slug=category_slug) 
        data = Book.objects.filter(category=category) 
    else:
        data = Book.objects.all()

    # If a search query is provided, filter books by title or category name
    if query:
        data = data.filter(title__icontains=query) | Book.objects.filter(category__name__icontains=query)

    categories = Category.objects.all()  # Get all categories

    return render(request, 'index.html', {'data': data, 'category': categories})



# def search(request):
#     return httpResponse('This is search');


