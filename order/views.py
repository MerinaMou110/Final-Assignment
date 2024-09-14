from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from library.models import Book
from .models import Order,Cart

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        # Check if the item is already in the cart
        if order.orderitems.filter(item=item).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
        else:
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart!")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item)
        messages.info(request, "This item was added to your cart!")

    return redirect('home')

@csrf_exempt
def cart_view(request, user_id, chk):
    user = User.objects.get(id=user_id)
    if chk == 0:
        messages.warning(request, "Your payment was not completed!")
    
    carts = Cart.objects.filter(user=user, purchased=False)
    orders = Order.objects.filter(user=user, ordered=False)
    print(carts) 
    
    if orders.exists():
        order = orders.first()
        context = {
            'carts': carts,
            'order': order
        }
        print(f"Context: {context}")

        return render(request, 'cart.html', context)
    else:
        messages.warning(request, "You do not have any items in your cart!")
        return redirect('home')

    
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order_item.delete()
            messages.warning(request, "This item was removed from your cart!")
            return redirect('order:cart', request.user.id, 1)
        else:
            messages.info(request, "This item was not in your cart!")
            return redirect('home')
    else:
        messages.info(request, "You do not have an active order!")
        return redirect('home')

    

@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.title} quantity has been updated")
        else:
            messages.info(request, f"{item.title} is not in your cart")
    else:
        messages.info(request, "You do not have an active order")

    return redirect("order:cart", request.user.id, 1)

        

@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Book, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.title} quantity has been updated")
            else:
                order_item.delete()
                messages.warning(request, f"{item.title} was removed from your cart!")

            return redirect("order:cart", request.user.id, 1)
        else:
            messages.info(request, f"{item.title} is not in your cart")
            return redirect('home')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('home')

