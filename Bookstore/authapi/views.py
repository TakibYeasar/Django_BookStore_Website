
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from store.models import *
from .models import *
from cart.models import *
from .forms import *
from django.contrib import messages
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})



@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(
            request, f"{product.title} has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, f"Added {product.title} to your WishList")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"section": "profile", "orders": orders})



@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})



@login_required
def delete_user(request):
    user = CustomUser.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")



def account_register(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
        else:
            return HttpResponse("Error handler content", status=400)
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})



def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def view_address(request):
    addresses = Address.objects.filter(CustomUser=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})



@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.CustomUser = request.user
            address.save()
            return redirect("account:addresses")
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})



@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, pk=id, CustomUser=request.user)
    if request.method == "POST":
        address_form = UserAddressForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            return redirect("account:addresses")
    else:
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, pk=id, CustomUser=request.user)
    address.delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(CustomUser=request.user,
                           default=True).update(default=False)
    address = get_object_or_404(Address, pk=id, CustomUser=request.user)
    address.default = True
    address.save()

    previous_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")
    return redirect("account:addresses")


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user, billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})
