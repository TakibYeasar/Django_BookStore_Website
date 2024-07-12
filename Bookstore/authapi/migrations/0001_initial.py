# Generated by Django 5.0.7 on 2024-07-12 16:58

import django.db.models.deletion
import django_countries.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email address"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=200, unique=True, verbose_name="Username"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="First Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Last Name"
                    ),
                ),
                ("password", models.CharField(max_length=255, verbose_name="Password")),
                (
                    "confirm_password",
                    models.CharField(max_length=255, verbose_name="Confirm Password"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "about_user",
                    models.TextField(blank=True, null=True, verbose_name="About User"),
                ),
                (
                    "address_one",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "address_two",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="Address"
                    ),
                ),
                ("postcode", models.CharField(max_length=50, verbose_name="Postcode")),
                ("city", models.CharField(blank=True, max_length=32, null=True)),
                ("state", models.CharField(blank=True, max_length=32, null=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("phone", models.CharField(blank=True, max_length=32)),
                (
                    "delivery_instructions",
                    models.CharField(
                        max_length=255, verbose_name="Delivery Instructions"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                ("default", models.BooleanField(default=False, verbose_name="Default")),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Address",
                "verbose_name_plural": "Addresses",
            },
        ),
    ]
