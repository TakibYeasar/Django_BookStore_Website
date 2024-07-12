from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from authapi.models import Address
from .models import DeliveryOptions
from basket.basket import Basket
import json
from django.http import JsonResponse
from cart.models import Order, OrderItem
from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest




@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    if request.method == 'POST' and request.POST.get("action") == "post":
        basket = Basket(request)
        delivery_option_id = int(request.POST.get("deliveryoption"))
        delivery_option = DeliveryOptions.objects.get(id=delivery_option_id)
        updated_total_price = basket.basket_update_delivery(
            delivery_option.delivery_price)

        request.session.setdefault("purchase", {})[
            "delivery_id"] = delivery_option.id

        return JsonResponse({"total": updated_total_price, "delivery_price": delivery_option.delivery_price})

    return JsonResponse({}, status=400)


@login_required
def delivery_address(request):
    if "purchase" not in request.session:
        messages.success(request, "Please select a delivery option")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    addresses = Address.objects.filter(
        customer=request.user).order_by("-default")

    if not addresses.exists():
        messages.success(request, "Please add an address")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    session = request.session
    session.setdefault("address", {})["address_id"] = str(addresses[0].id)

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    if "address" not in request.session:
        messages.success(request, "Please select an address")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    return render(request, "checkout/payment_selection.html", {})


@login_required
def payment_complete(request):
    if request.method == 'POST':
        PPClient = PayPalClient()
        body = json.loads(request.body)
        order_id = body.get("orderID")
        user_id = request.user.id

        request_order = OrdersGetRequest(order_id)
        response = PPClient.client.execute(request_order)

        if response.result.status == 'COMPLETED':
            basket = Basket(request)
            order = Order.objects.create(
                user_id=user_id,
                full_name=response.result.purchase_units[0].shipping.name.full_name,
                email=response.result.payer.email_address,
                address1=response.result.purchase_units[0].shipping.address.address_line_1,
                address2=response.result.purchase_units[0].shipping.address.admin_area_2,
                postal_code=response.result.purchase_units[0].shipping.address.postal_code,
                country_code=response.result.purchase_units[0].shipping.address.country_code,
                total_paid=response.result.purchase_units[0].amount.value,
                order_key=response.result.id,
                payment_option="paypal",
                billing_status=True,
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"]
                )

            return JsonResponse("Payment completed!", safe=False)
        else:
            return JsonResponse("Payment not completed!", status=400)

    return JsonResponse({}, status=400)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
