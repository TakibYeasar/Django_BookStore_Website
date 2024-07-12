import pytest
from django.test import Client
from authapi.forms import RegistrationForm, UserAddressForm
from store.models import Customer


@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        ("mike", "02343343434", "add1", "add2", "town", "postcode", True),
        ("", "02343343434", "add1", "add2", "town", "postcode", False),
    ],
)
def test_customer_add(full_name, phone, address_line, address_line2, town_city, postcode, validity):
    form_data = {
        "full_name": full_name,
        "phone": phone,
        "address_line": address_line,
        "address_line2": address_line2,
        "town_city": town_city,
        "postcode": postcode,
    }
    form = UserAddressForm(data=form_data)
    assert form.is_valid() is validity


@pytest.mark.django_db
def test_customer_create_address(client, customer):
    user = customer
    client.force_login(user)
    form_data = {
        "full_name": "test",
        "phone": "test",
        "address_line": "test",
        "address_line2": "test",
        "town_city": "test",
        "postcode": "test",
    }
    response = client.post("/account/add_address/", data=form_data)
    assert response.status_code == 302  # Redirect status


@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", True),
        ("user1", "a@a.com", "12345a", "", False),  # no second password
        # ("user1", "a@a.com", "", "12345a", False),  # no first password
        ("user1", "a@a.com", "12345a", "12345b", False),  # password mismatch
        ("user1", "a@.com", "12345a", "12345a", False),  # invalid email
    ],
)
@pytest.mark.django_db
def test_create_account(user_name, email, password, password2, validity):
    form_data = {
        "user_name": user_name,
        "email": email,
        "password": password,
        "password2": password2,
    }
    form = RegistrationForm(data=form_data)
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "user_name, email, password, password2, expected_status",
    [
        ("user1", "a@a.com", "12345a", "12345a", 200),
        ("user1", "a@a.com", "12345a", "12345", 400),
        ("user1", "", "12345a", "12345", 400),
    ],
)
@pytest.mark.django_db
def test_create_account_view(client, user_name, email, password, password2, expected_status):
    form_data = {
        "user_name": user_name,
        "email": email,
        "password": password,
        "password2": password2,
    }
    response = client.post("/account/register/", data=form_data)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_account_register_redirect(client, customer):
    user = customer
    client.force_login(user)
    response = client.get("/account/register/")
    assert response.status_code == 302  # Redirect status


@pytest.mark.django_db
def test_account_register_render(client):
    response = client.get("/account/register/")
    assert response.status_code == 200


