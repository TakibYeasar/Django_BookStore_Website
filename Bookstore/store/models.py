from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category model implemented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category Safe URL"),
        max_length=255,
        unique=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    ProductType model providing a list of different product types.
    """

    name = models.CharField(
        verbose_name=_("Product Type Name"),
        help_text=_("Required"),
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    ProductSpecification model containing product specifications or features.
    """

    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model containing all product items.
    """

    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Not Required"),
        blank=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 999.99"),
        max_digits=6,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("Maximum 999.99"),
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    ProductSpecificationValue model holding each product's specification values.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specification_values"
    )
    specification = models.ForeignKey(
        ProductSpecification, on_delete=models.CASCADE, related_name="specification_values"
    )
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (maximum 255 characters)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    ProductImage model representing images associated with a product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative Text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Image for {self.product.title}"
