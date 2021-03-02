from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Category, Customer, ShippingAddress, Order, OrderItem, Coupon, User
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('store:index')
        self.cart_url = reverse('store:cart')
        self.add_to_cart_url = reverse('store:addtocart', args=["test"])
        self.product_test = Product.objects.create(
            title='test',
            description = 'desc',
        )
        self.order_cancel_url = reverse('store:ordercancel', args=[2])
        
        

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_cart_get(self):
        response = self.client.get(self.cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_add_to_cart_get(self):
        response = self.client.get(self.add_to_cart_url)
        response2 = self.client.get(response.url)
       

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'store/cart.html')

    def test_order_cancel_get(self):
        response = self.client.get(self.order_cancel_url)
        response2 = self.client.get(response.url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'store/cart.html')

    def test_order_cancel_post(self):
        Order.objects.create(
            id = 2
        )


        response = self.client.post(self.order_cancel_url)
        response2 = self.client.get(response.url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 200)

        self.order = Order.objects.filter(id=2)
        self.assertEquals(len(self.order), 0)

        self.assertTemplateUsed(response2, 'store/cart.html')

    def test_order_cancel_post_error(self):
        Order.objects.create(
            id = 1
        )

        response = self.client.post(self.order_cancel_url)

        self.assertEquals(response.status_code, 404)