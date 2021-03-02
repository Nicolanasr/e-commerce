from django.test import TestCase
from django.test.testcases import SimpleTestCase
from django.urls import reverse, resolve
from store.views import index, cart, checkout, trackorderred, track_order, apply_coupon, remove_coupon, addProduct, addtocart,trackorder, ordercancel


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('store:index')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, index )

    def test_cart_url_is_resolved(self):
        url = reverse('store:cart')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, cart )

    def test_addtocart_url_is_resolved(self):
        url = reverse('store:addtocart', args=[1])
        #print(resolve(url))
        self.assertEquals(resolve(url).func, addtocart )

    def test_checkout_url_is_resolved(self):
        url = reverse('store:checkout')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, checkout )

    def test_trackorderred_url_is_resolved(self):
        url = reverse('store:trackorderred')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, trackorderred)

    def test_track_order_url_is_resolved(self):
        url = reverse('store:track_order')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, track_order)

    def test_trackorder_url_is_resolved(self):
        url = reverse('store:trackorder', args=[1])
        #print(resolve(url))
        self.assertEquals(resolve(url).func, trackorder)

    def test_apply_coupon_url_is_resolved(self):
        url = reverse('store:apply_coupon')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, apply_coupon)

    def test_remove_coupon_url_is_resolved(self):
        url = reverse('store:remove_coupon')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, remove_coupon)

    def test_addProduct_url_is_resolved(self):
        url = reverse('store:addProduct')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, addProduct)

    def test_ordercancel_url_is_resolved(self):
        url = reverse('store:ordercancel', args=[1])
        #print(resolve(url))
        self.assertEquals(resolve(url).func, ordercancel)

