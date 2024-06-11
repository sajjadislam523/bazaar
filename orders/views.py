from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account
from django.contrib import messages, auth
from .ssl import sslcommerz_payment_gateway

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutSuccessView(View):
    model = Payment
    template_name = 'orders/success.html'
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            user_id = int(data['value_a'])
            user = Account.objects.get(pk=user_id)
            order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_b'])

            payment = Payment(
                user=user,
                payment_id=data['tran_id'],
                payment_method=data['card_type'],
                amount_paid=order.order_total,
                status=data['status'],
            )
            payment.save()

            order.payment = payment
            order.is_ordered = True
            order.save()

            cart_items = CartItem.objects.filter(user=user)
            for item in cart_items:
                order_product = OrderProduct(
                    order=order,
                    payment=payment,
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True,
                )
                order_product.save()

                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            CartItem.objects.filter(user=user).delete()

            auth.login(request, user)
            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_received_email.html', {
                'user': user,
                'order': order,
            })
            to_email = data['value_c']
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            url = reverse('order_complete') + f'?order_id={order.order_number}&transaction_id={payment.payment_id}'
            return redirect(url)

        except Exception as e:
            messages.error(request, 'Something went wrong')
            print(e)  # Log the exception for debugging

        return render(request, 'orders/success.html')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFailedView(View):
    template_name = 'orders/failed.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = current_user
            order.order_total = grand_total
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()

            order_number = datetime.datetime.now().strftime('%Y%m%d') + str(order.id)
            order.order_number = order_number
            order.save()

            return redirect(sslcommerz_payment_gateway(request, order_number, str(current_user.id), grand_total, order.email))

    return render(request, 'orders/payments.html')


def order_complete(request):
    order_number = request.GET.get('order_id')
    transID = request.GET.get('transaction_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = sum(i.product_price * i.quantity for i in ordered_products)
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')