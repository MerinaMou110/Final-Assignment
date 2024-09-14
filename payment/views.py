from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from order.models import Order
from order.models import Cart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from sslcommerz_lib import SSLCOMMERZ
from django.contrib.auth.decorators import login_required
import uuid

def unique_transaction_id_generator():
    return str(uuid.uuid4())  # Generates a unique transaction ID

@login_required
def checkout(request):
    # Fetch the user's active order (if any)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.orderitems.all()
        order_total = order.get_totals()
    except Order.DoesNotExist:
        order_items = []
        order_total = 0

    context = {
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'checkout.html', context)

def payment(request):
    order = Order.objects.get(user=request.user, ordered=False)
 
    order_items = order.orderitems.all()
    order_total = order.get_totals() 
    order.total_amount = order_total  # Ensure total_amount is updated 
    order.save()

    settings = { 'store_id': 'bookd66e4226b7822b', 'store_pass': 'bookd66e4226b7822b@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    tran_id = unique_transaction_id_generator()
    post_body = {
        'total_amount': order_total,
        'currency': "BDT",
        'tran_id': tran_id,
        'success_url': f"http://127.0.0.1:8000/payment/purchase/{tran_id}/{request.user.id}/",
        'fail_url': "http://127.0.0.1:8000/library/cart/",
        'cancel_url': "http://127.0.0.1:8000/payment/",
        'emi_option': 0,
        'cus_name': request.user.username,
        'cus_email': request.user.email,
        'cus_phone':  request.user.account.phone_num,
        'cus_add1': "Khulna",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",
    }

    response = sslcz.createSession(post_body)
    print(response)
    return redirect(response['GatewayPageURL'])

@csrf_exempt
def purchase(request, trans_id, user_id):
    try:
        # Fetch the user and their order
        user = User.objects.get(id=user_id)
        order = Order.objects.get(user=user, ordered=False)

        # Update order status
        order.ordered = True
        order.order_id = trans_id
        order.payment_id = trans_id
        order.save()

        # Fetch and update cart items
        cart_items = Cart.objects.filter(user=user, purchased=False)
        for item in cart_items:
            item.purchased = True
            item.save()
            
            # Update book quantity
            book = item.item
            if book.available_copies >= item.quantity:
                book.available_copies -= item.quantity
                book.save()
            else:
                # Handle case where not enough copies are available
                messages.error(request, f"Not enough copies available for book: {book.title}")

        return HttpResponseRedirect(reverse('payment:ordersitem'))
    except (User.DoesNotExist, Order.DoesNotExist):
        messages.error(request, "Order or user not found.")
        return redirect('home')


@csrf_exempt
def view_order(request):
    orders = Order.objects.filter(user=request.user, ordered=True)

    if orders.exists():  # Check if any orders exist
        context = {
            'orders': orders,
        }
    else:
        messages.warning(request, "You do not have any orders!")
        return redirect('home')

    return render(request, 'order.html', context)
