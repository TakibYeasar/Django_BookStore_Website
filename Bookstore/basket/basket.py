from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404
from store.models import Product
from checkout.models import DeliveryOptions


class Basket:
    """
    A base Basket class, providing default behaviors for managing a user's shopping basket.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Add or update a product in the basket.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(
                product.regular_price), "qty": qty}

        self.save()

    def __iter__(self):
        """
        Iterate over items in the basket and retrieve corresponding Product objects.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the total number of items in the basket.
        """
        return sum(item["qty"] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update the quantity of a product in the basket.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    def get_subtotal_price(self):
        """
        Calculate and return the subtotal price of items in the basket.
        """
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    def get_delivery_price(self):
        """
        Retrieve and return the delivery price from session data.
        """
        newprice = 0.00

        if "purchase" in self.session:
            delivery_id = self.session["purchase"].get("delivery_id")
            if delivery_id:
                delivery_option = get_object_or_404(
                    DeliveryOptions, id=delivery_id)
                newprice = delivery_option.delivery_price

        return newprice

    def get_total_price(self):
        """
        Calculate and return the total price including subtotal and delivery price.
        """
        subtotal = sum(Decimal(item["price"]) * item["qty"]
                       for item in self.basket.values())
        delivery_price = self.get_delivery_price()
        total = subtotal + Decimal(delivery_price)
        return total

    def basket_update_delivery(self, deliveryprice=0):
        """
        Update the total price of the basket with a specified delivery price.
        """
        subtotal = sum(Decimal(item["price"]) * item["qty"]
                       for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def delete(self, product):
        """
        Delete a product from the basket.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        """
        Clear all items and related session data from the basket.
        """
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()

    def save(self):
        """
        Save the basket session.
        """
        self.session.modified = True
