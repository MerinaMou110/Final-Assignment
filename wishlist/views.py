from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from wishlist.forms import WishlistForm
from library.models import Book

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    return render(request, 'cart.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, book_id):
    if request.method == 'POST':
        Wishlist.objects.create(user=request.user, book_id=book_id)
    return redirect('wishlist')
    

@login_required
def remove_from_wishlist(request, wishlist_id):
    Wishlist.objects.filter(id=wishlist_id).delete()
    return redirect('wishlist')