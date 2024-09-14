from django.urls import path
from payment import views
app_name='payment'
urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('pay/',views.payment,name='payment'),
    path('purchase/<trans_id>/<int:user_id>/',views.purchase,name='purchase'),
    path('orders/',views.view_order,name='ordersitem'),
]
