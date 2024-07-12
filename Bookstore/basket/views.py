from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/summary.html", {"basket": basket})


def basket_add(request):
    basket = Basket(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basket_qty = len(basket)
        response = JsonResponse({"qty": basket_qty})
        return response
    return JsonResponse({"error": "Invalid request method or parameters"})


def basket_delete(request):
    basket = Basket(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)

        basket_qty = len(basket)
        basket_total = basket.get_total_price()
        response = JsonResponse({"qty": basket_qty, "subtotal": basket_total})
        return response
    return JsonResponse({"error": "Invalid request method or parameters"})


def basket_update(request):
    basket = Basket(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        basket.update(product=product_id, qty=product_qty)

        basket_qty = len(basket)
        basket_subtotal = basket.get_subtotal_price()
        response = JsonResponse(
            {"qty": basket_qty, "subtotal": basket_subtotal})
        return response
    return JsonResponse({"error": "Invalid request method or parameters"})
