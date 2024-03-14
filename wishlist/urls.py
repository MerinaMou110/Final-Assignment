# urls.py

from django.urls import path
from .views import wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('wishlist/', wishlist, name='wishlist'),
    path('add_to_wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
