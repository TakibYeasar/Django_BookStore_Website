import factory
from faker import Faker

from authapi.models import Address, Customer
from store.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

fake = Faker()

####
# gue
####


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "django"
    slug = "django"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "book"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "pages"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product_title"
    description = factory.LazyFunction(fake.text)
    slug = "product_slug"
    regular_price = 9.99
    discount_price = 4.99


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "100"


####
# Account
####


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = "a@a.com"
    name = "user1"
    mobile = "07525251252"
    password = factory.PostGenerationMethodCall('set_password', 'tester')
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    full_name = factory.LazyFunction(fake.name)
    phone = factory.LazyFunction(fake.phone_number)
    postcode = factory.LazyFunction(fake.postcode)
    address_line = factory.LazyFunction(fake.street_address)
    address_line2 = factory.LazyFunction(fake.street_address)
    town_city = factory.LazyFunction(fake.city_suffix)


