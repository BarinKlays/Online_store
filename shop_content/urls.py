from django.urls import path

from shop_content.views import *

urlpatterns = [
    path('', IndexViewShop, name='shopindex'),
    path('ProductView/', ProductView, name='productview'),
    path('ProductView/?gen=Men', ProductView, name='?gen=Men'),
    path('ProductDetail/<int:pk>/', ProductDetail, name='productdetail'),
    path('Profil/', ProfileUser, name='profileuser'),
    # path('EditProfile/', EditProfile, name='editprofile'),

    path('get_product_info/', ProductDetail, name='get_product_info'),
    path('toggle_favorite/', toggle_favorite, name='toggle_favorite'),

    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('Corzina/', Corzina, name='Corzina'),
    path('About/', About, name='about'),
    path('ContactView/', ContactView, name='contactview'),
    path('BasketView/', BasketView, name='basketview'),
    path('BasketView/remove/<int:pk>/', Remove_From_Cart, name='Remove_From_Cart'),
    path('favorite/', FavoriteView, name='favorite'),
]