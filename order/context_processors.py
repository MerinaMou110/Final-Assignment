from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        # Count only items in the cart that have not been purchased
        cart_count = Cart.objects.filter(user=request.user, purchased=False).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
