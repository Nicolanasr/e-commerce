from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import DO_NOTHING, SET_DEFAULT, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Customer(models.Model):
    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return str(self.uid)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    uid = models.CharField(max_length=500, null=True, blank=True)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)


class Product(models.Model):
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    qty = models.IntegerField(null=True, blank=True)
    price = models.FloatField(default=1)
    image = models.ImageField(upload_to='images/')
    ratings = models.FloatField(null=True, blank=True)
    avg_ratings = models.FloatField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Rating(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    product_rated = models.ForeignKey(Product, on_delete=SET_NULL, null=True, blank=True)
    customer_rated = models.ForeignKey(Customer, on_delete=DO_NOTHING, null=True, blank=True)



class ShippingAddress(models.Model):
    def __str__(self):
        return self.address

    address = models.CharField(max_length=200)
    address2 = models.TextField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)


class Coupon(models.Model):
    def __str__(self):
        return self.coupon

    coupon = models.CharField(max_length=50)
    value = models.FloatField()


class Order(models.Model):
    def __str__(self):
        return str(self.id)

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)

    address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)

    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    coupon_activated = models.BooleanField(
        default=False, null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True, blank=True)
    totalAfterCoupon = models.FloatField(null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    shipped = models.BooleanField(default=False, null=True, blank=False)
    deliveryDate = models.DateField(null=True, blank=True)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(
        default=1,  validators=[MinValueValidator(1), MaxValueValidator(100)])

    @property
    def getTotal(self):
        return self.product.price * self.quantity


def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance, name=instance.username, email=instance.email)


post_save.connect(create_customer, sender=User)


def update_customer(sender, instance, created, **kwargs):
    if created == False:
        print(instance)
        Customer.objects.select_for_update().filter(user=instance).update(
            user=instance, name=instance.username, email=instance.email)


post_save.connect(update_customer, sender=User)
