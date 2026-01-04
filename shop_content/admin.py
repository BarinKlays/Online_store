from django.contrib import admin

# Register your models here.
from shop_content.models import *
from common.models import *

admin.site.register(CartItem),
admin.site.register(Cart),
admin.site.register(Favorite),
admin.site.register(Sub),
admin.site.register(CountryBasket),
admin.site.register(Basket),