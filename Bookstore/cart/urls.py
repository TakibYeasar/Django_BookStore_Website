from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('', views.basket_view, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.ErrorView.as_view(), name='error'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
