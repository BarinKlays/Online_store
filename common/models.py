from os.path import basename

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta



class Brand(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'common'
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        app_label = 'common'
    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        app_label = 'common'
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    class Meta:
        app_label = 'common'
    def __str__(self):
        return self.category_name

class Size(models.Model):
    size_value = models.CharField(max_length=5)
    class Meta:
        app_label = 'common'
    def __str__(self):
        return self.size_value

class Color(models.Model):
    color_name = models.CharField(max_length=20)
    class Meta:
        app_label = 'common'

    def __str__(self):
        return self.color_name

class Product(models.Model):
    GENDER = {
        ('Men', 'Мужское'),
        ('Women', 'Женское'),
    }
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER)
    available_sizes = models.ManyToManyField(Size)
    available_colors = models.ManyToManyField(Color )
    date_added = models.DateTimeField(default=timezone.now)
    availability = models.BooleanField()
    seasons = models.ManyToManyField(Season)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    popularity = models.IntegerField(default=0)

    def favoriteduser(item, user):
        return Favorite.objects.filter(user=user, product=item).exists()

    class Meta:
        app_label = 'common'

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorited_by', on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'product')
        app_label = 'common'

    def __str__(self):
        return f"{self.user.username} likes {self.product.name}"



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        app_label = 'common'

    def __str__(self):
        return self.image.url

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='AboutUs/')

    subtitle = models.CharField(max_length=255)
    ourstory = models.TextField()
    ourstorytwo = models.TextField()
    ourstorytree = models.TextField()
    ourstoryimg = models.ImageField(upload_to='AboutUs/OurStoryqq')

    ourmission = models.CharField(max_length=255)
    ourmissiontwo = models.TextField()
    quote = models.TextField()
    author = models.CharField(max_length=255, default='steav')

    ourmissionimg = models.ImageField(upload_to='AboutUs/ourmission')

    class Meta:
        app_label = 'common'

class Contact(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='Contact/')

    adress = models.CharField(max_length=255)
    talk = models.CharField(max_length=255)
    support = models.EmailField()

    class Meta:
        app_label = 'common'

class FeedBack(models.Model):
    feedemail = models.EmailField()
    text = models.TextField()


    class Meta:
        app_label = 'common'








