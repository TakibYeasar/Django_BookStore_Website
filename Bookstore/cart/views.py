from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from basket.basket import Basket
from .models import Order, OrderItem
import json
import stripe
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


@login_required
def basket_view(request):
    basket = Basket(request)
    total = str(basket.get_total_price()).replace('.', '')
    total = int(total)

    stripe.api_key = ''  # Add your Stripe API key here
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def add(request):
    if request.method == 'POST' and request.POST.get('action') == 'post':
        basket = Basket(request)
        order_key = request.POST.get('order_key')
        user_id = request.user.id
        basket_total = basket.get_total_price()

        # Check if order exists
        if not Order.objects.filter(order_key=order_key).exists():
            order = Order.objects.create(
                user_id=user_id,
                full_name='name',  # Replace with actual name
                address1='add1',   # Replace with actual address
                address2='add2',   # Replace with actual address
                total_paid=basket_total,
                order_key=order_key
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

        # Adjust response as needed
        return JsonResponse({'success': 'Return something'})


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id, billing_status=True)
    return orders


@login_required
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


class ErrorView(TemplateView):
    template_name = 'payment/error.html'
