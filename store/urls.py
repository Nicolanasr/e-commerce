from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'store'

urlpatterns = [
    path('test/', views.test, name="test"),
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('<slug:orderid>/ordercancel/', views.ordercancel, name="ordercancel"),
    path('checkout/', views.checkout, name="checkout"),
    path('addtocart/<item>/', views.addtocart, name="addtocart"),
    path('trackorderred/', views.trackorderred, name="trackorderred"),
    path('trackorder/', views.track_order, name="track_order"),
    path('trackorder/<slug:order_track>', views.trackorder, name="trackorder"),
    path('apply_coupon/', views.apply_coupon, name="apply_coupon"),
    path('remove_coupon/', views.remove_coupon, name="remove_coupon"),
    path('add_product/', views.addProduct, name="addProduct"),
    path('rate_product/', views.rate_product, name="rate_product"),
    path('product/<int:product_id>', views.viewProduct, name="viewProduct"),
    path('api/products', views.productsApi, name='productApi'), 
    path('api/', views.api, name='api'), 
    path('api/products/<str:pk>', views.singleProductApi, name='singleProductApi'), 
]
