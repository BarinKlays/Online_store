from shop_content.views import IndexViewShop
from .views import *
from django.urls import path

urlpatterns = [
    path('', IndexViewShop, name='indexshop'),
    path('adminka/', Adminka, name='adminka'),
    path('product_list/', ProductList, name='product_list'),
    path('product_list/add_product/', AddProduct, name='add_product'),
    path('product_list/product_edit/<int:pk>', ProductEdit, name='product_edit'),
    path('product_list/product_detail/<int:pk>', Product_detail, name='product_detail'),
    path('product_list/delete_product/<int:pk>', Delete_Product, name='Delete_Product'),
    path('user_list/', UserList.as_view(), name='user_list'),
    path('dashboard/', DashBoard, name='dashboard'),



    path('orderhandler/UpladedOrder/<int:pk>', UpladedOrder, name='UpladedOrder'),
    path('orderhandler/YpokovOrder/<int:pk>', YpokovOrder, name='YpokovOrder'),
    path('orderhandler/OtpravkaOrder/<int:pk>', OtpravkaOrder, name='OtpravkaOrder'),
    path('orderhandler/CompletedOrder/<int:pk>', CompletedOrder, name='CompletedOrder'),

# page
    path('brand/', Brand_view, name='brand'),
    path('size/', Size_view, name='size'),
    path('colors/', Colors_view, name='colors'),
    path('sesons/', Sesons_view, name='sesons'),
    path('country/', Country_view, name='country'),
    path('slider/', Slider, name='slider'),
    path('AboutView/', AboutView, name='aboutview'),
    path('ContactView/', ContactView, name='contactviewadmin'),
    path('editcontact/', EditContact, name='editcontact'),
    path('FeedBackview/', FeedBackview, name='feedback'),
    path('orderhandler/', OrderHandler, name='orderhandler'),

# add
    path('brand/add_brand/', AddBrand, name='addbrend'),
    path('size/add_Size/', Add_Size, name='addsize'),
    path('colors/add_colors/', AddColors, name='addcolors'),
    path('sesons/add_sesons/', AddSesons, name='addsesons'),
    path('country/add_country/', AddCountry, name='addcountry'),
    path('slider/AddSlider/', AddSliderView, name='addslider'),

# edit
    path('brand/edit_brand/<int:pk>', EditBrand, name='editbrand'),
    path('size/edit_size/<int:pk>', Edit_Size, name='editsize'),
    path('colors/edit_colors/<int:pk>', ColorsEdit, name='editcolors'),
    path('sesons/edit_sesons/<int:pk>', SesonsEdit, name='editsesons'),
    path('country/edit_country/<int:pk>', CountryEdit, name='editcountry'),
    path('slider/EditSlider/<int:pk>', EditSlider, name='editslider'),
    path('slider/EditAbout/', EditAbout, name='editabout'),

# delete
    path('brand/delete_brand/<int:pk>', DeleteBrand, name='deletebrand'),
    path('size/delete_size/<int:pk>', DeleteSize, name='deletesize'),
    path('colors/delete_colors/<int:pk>', DeleteColors, name='deletecolors'),
    path('sesons/delete_sesons/<int:pk>', DeleteSesons, name='deletesesons'),
    path('country/delete_country/<int:pk>', DeleteCountry, name='deletecountry'),
    path('slider/DeleteSlider/<int:pk>', DeleteSlider, name='deleteslider'),

]
