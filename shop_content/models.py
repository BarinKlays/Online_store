from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from common.models import *


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'shop_content'

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        app_label = 'shop_content'

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name} (Size: {self.size}, Color: {self.color})"

class CountryBasket(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Basket(models.Model):
    STATUS = {
        ('New','Новый'),
        ('Search','Ищем товар'),
        ('Ypokov','Упаковаем'),
        ('Otpravka','Отправляем'),
        ('Completed','Заказ доставлен'),
    }
    user = models.ForeignKey(User, related_name='baskets', on_delete=models.CASCADE)
    cart = models.ManyToManyField('CartItem', related_name='baskets')
    country_basket = models.ForeignKey(CountryBasket, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    postcode = models.IntegerField()
    status = models.CharField(max_length=255, choices=STATUS, default='New')

    def __str__(self):
        return f" {self.user.username} {self.cart}"



class Slaider(models.Model):
    img = models.ImageField(upload_to='slider/')
    subtext = models.CharField(max_length=255)
    main_text = models.CharField(max_length=255)
    class Meta:
        app_label = 'shop_content'


class Sub(models.Model):
    email = models.EmailField(unique=True)




