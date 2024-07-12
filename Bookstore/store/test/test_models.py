from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(
            reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        cls.data1 = Product.objects.create(category=category, title='django beginners', created_by_id=1,
                                           slug='django-beginners', price='20.00', image='django')
        cls.data2 = Product.objects.create(category=category, title='django advanced', created_by_id=1,
                                           slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data1
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/django-beginners')
        response = self.client.post(
            reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        """
        Test product model custom manager returns only active products
        """
        data = Product.products.active()
        self.assertEqual(data.count(), 1)


# def test_category_str(product_category):
#     assert str(product_category) == "django"


# def test_category_reverse(client, product_category):
#     url = reverse("store:category_list", args=[product_category.slug])
#     response = client.get(url)
#     assert response.status_code == 200


# def test_producttype_str(product_type):
#     assert str(product_type) == "book"


# def test_product_spec_str(product_specification):
#     assert str(product_specification) == "pages"


# def test_product_str(product):
#     assert str(product) == "product_title"


# def test_product_url_resolve(client, product):
#     url = reverse("store:product_detail", args=[product.slug])
#     response = client.get(url)
#     assert response.status_code == 200


# def test_product_specification_value(product_spec_value):
#     assert str(product_spec_value) == "100"
