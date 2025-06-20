import pytest
from authapi.models import Customer, Address


@pytest.mark.django_db
def test_customer_str(customer):
    assert str(customer) == "user1"


@pytest.mark.django_db
def test_adminuser_str(adminuser):
    assert str(adminuser) == "admin_user"


@pytest.mark.django_db
def test_customer_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="")
    assert str(e.value) == "Customer Account: You must provide an email address"


@pytest.mark.django_db
def test_customer_email_incorrect(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="a.com")
    assert str(e.value) == "You must provide a valid email address"


@pytest.mark.django_db
def test_adminuser_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="", is_superuser=True, is_staff=True)
    assert str(e.value) == "Superuser Account: You must provide an email address"


@pytest.mark.django_db
def test_adminuser_email_incorrect(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(
            email="a.com", is_superuser=True, is_staff=True)
    assert str(e.value) == "You must provide a valid email address"


@pytest.mark.django_db
def test_adminuser_email_not_staff(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="", is_superuser=True, is_staff=False)
    assert str(e.value) == "Superuser must be assigned to is_staff=True"


@pytest.mark.django_db
def test_adminuser_email_not_superuser(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(
            email="a.com", is_superuser=False, is_staff=True)
    assert str(e.value) == "Superuser must be assigned to is_superuser=True"


@pytest.mark.django_db
def test_address_str(address):
    name = address.full_name
    assert str(address) == f"{name} Address"


