from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.forms import RegisterForm
from accounts.models import UserInfo
from common.models import Product, ProductImage
from shop_content.forms import *
from shop_content.models import *
from common.models import *


def ProfileUser(request):
    user = User.objects.get(username=request.user)
    basket = Basket.objects.filter(user=request.user)
    try:
        userinfo = UserInfo.objects.get(user=user)
        user_info = {'info': userinfo, 'username': user}
    except UserInfo.DoesNotExist:
        user_info = {'info': '0', 'username': user}

    print(user_info)

    context = {
        'user_info': user_info,
        'basket': basket
    }

    return render(request, 'shop/profileuser.html', context)

# def EditProfile(request):
#
#     user = User.objects.get(username=request.user)
#
#     try:
#         userinfo = UserInfo.objects.get(user=user)
#         user_info = {'info': userinfo, 'username': user}
#     except UserInfo.DoesNotExist:
#         user_info = {'info': '0', 'username': user}
#     if request.method == 'POST':
#         form = EidtRegisterForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             if 'images' in request.FILES:
#                 user.userinfo.images = request.FILES['images']
#                 user.save()
#             return redirect('profileuser')
#     else:
#         form = EidtRegisterForm(instance=request.user)
#
#     context = {
#         'form': form,
#         'user_info': user_info
#     }
#
#     print(form)
#
#     return render(request, 'shop/editprofile.html', context)

def FavoriteView(request):
    favorite = Favorite.objects.all().filter(user=request.user)

    product_list = []
    for item in favorite:
        favorite_name = item.product
        is_favorited = favorite_name.favoriteduser(request.user)
        product_images = ProductImage.objects.filter(product__pk=favorite_name.pk)
        product_list.append({'productimage': product_images, 'info': favorite_name, is_favorited:'is_favorited'})
        print(is_favorited)

    context = {
        'product_list': product_list
    }

    return render(request, 'shop/favorite.html', context)

# def BaseShop(request):
#     if request.method == 'POST':
#         form = SubForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             if Sub.objects.filter(email=email).exists():
#                 messages.error(request, 'Такой email уже существует')
#             else:
#                 form.save()
#                 messages.success(request, 'Успешно подписались')
#                 return redirect('shopindex')
#     else:
#         messages.error(request, 'Вы уже подписались')
#         form = SubForm()
#
#     context = {
#         'form':form
#     }
#
#     print(form)
#
#     return render(request, 'shop/shop.html', context)


def IndexViewShop(request):
    sliders = Slaider.objects.all()
    category = Category.objects.all()
    product_list = Product.objects.all()


    products_with_images = []
    for product in product_list:
        products_image = ProductImage.objects.filter(product__pk=product.pk)
        if request.user.is_authenticated:
            try:
                is_favorited = product.favoriteduser(request.user)
            except product.DoesNotExist:
                is_favorited = False
        else:
            is_favorited = None
        products_with_images.append({'productimage': products_image, 'info': product, 'is_favorited': is_favorited})

        print(is_favorited)

    selected_category = request.GET.get('category', 0)

    if selected_category:
        products_with_images = [product for product in products_with_images if
                                product['info'].category.category_name == selected_category]
        print(product_list)

    sorted_categories = category.order_by('category_name')

    context = {
        'sliders': sliders,
        'sorted': sorted_categories,
        'product_list': products_with_images,
        'selected_category': selected_category,

    }


    return render(request, 'shop/index.html', context)

def About(request):
    try:
        about = AboutUs.objects.get()
    except AboutUs.DoesNotExist:
        about = None
    context = {
        'about':about
    }
    print(about)
    return render(request, 'shop/about.html', context )

def ContactView(request):
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contactview')

    else:
        form = FeedBackForm()

    try:
        contact = Contact.objects.get()
    except Contact.DoesNotExist:
        contact = None

    context = {
        'contact': contact,
        'form':form
    }

    return render(request, 'shop/contact.html', context)

def BasketView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    country = CountryBasket.objects.all()
    cart_items = CartItem.objects.filter(cart=cart)


    product_list = []
    for cart_item in cart_items:
        productsimage = ProductImage.objects.filter(product__pk=cart_item.product.pk)
        total_price = cart_item.product.price * cart_item.quantity
        product_list.append({'productimage': productsimage, 'info': cart_item.product, 'col': cart_item.quantity, 'total_price': total_price})


    if request.method == 'POST':
        form = BasketForm(request.POST)
        if form.is_valid():
            basket = form.save(commit=False)
            basket.user = request.user
            basket.save()
            for cart_item_id in cart_items:
                basket.cart.add(cart_item_id)
            return redirect('basketview')
    else:
        form = BasketForm()

    context = {
        'cart':cart,
        'country': country,
        'product_list':product_list,
        'form': form
    }

    print(form)

    return render(request, 'shop/shoping-cart.html', context)


def Remove_From_Cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    cart_item = get_object_or_404(CartItem, cart=cart, pk=pk)
    cart_item.delete()

    return redirect('basketview')



def ProductView(request):
    product = Product.objects.all()
    colors = Color.objects.all()

    gen_filter = request.GET.get('gen', None)
    price_filter = request.GET.get('price')
    color_filter = request.GET.get('color')
    sort_filter = request.GET.get('sort')
    query = request.GET.get('search-product')

    if gen_filter:
        product = product.filter(gender=gen_filter)

    if sort_filter:
        if sort_filter == 'popular':
            product = product.order_by('-popularity')
        elif sort_filter == 'high_rating':
            product = product.order_by('-rating')
        elif sort_filter == 'newest':
            product = product.order_by('-date_added')
        elif sort_filter == 'price_low_to_high':
            product = product.order_by('price')
        elif sort_filter == 'price_high_to_low':
            product = product.order_by('-price')

    if price_filter:
        if price_filter == '0-50':
            product = product.filter(price__gte=0, price__lte=50)
        elif price_filter == '50-100':
            product = product.filter(price__gte=50, price__lte=100)
        elif price_filter == '100-150':
            product = product.filter(price__gte=100, price__lte=150)
        elif price_filter == '150-200':
            product = product.filter(price__gte=150, price__lte=200)
        elif price_filter == '200_plus':
            product = product.filter(price__gte=200)

    if color_filter:
        product = product.filter(available_colors__color_name=color_filter)

    if query:
        product = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    product_list = []
    for item in product:
        productsimage = ProductImage.objects.filter(product__pk=item.pk)
        if request.user.is_authenticated:
            try:
                is_favorited = item.favoriteduser(request.user)
            except item.DoesNotExist:
                is_favorited = False
        else:
            is_favorited = None

        product_list.append({'productimage': productsimage, 'info': item, 'is_favorited': is_favorited})
        print(product_list)

    context = {
        'gen_filter': gen_filter,
        'product_list' : product_list,
        'selected_sort': sort_filter,
        'selected_price': price_filter,
        'selected_color': color_filter,
        'colors': colors,
    }
    print(gen_filter)

    return render(request, 'shop/product.html', context)


def get_product_info(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(pk=product_id)

    # Получаем изображения товара
    product_images = ProductImage.objects.filter(product=product)

    # Формируем список URL изображений
    image_urls = [image.image.url for image in product_images]

    # Формируем данные для ответа
    data = {
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'images': image_urls,
        # Другие поля товара, которые вы хотите отправить
        # Другие поля товара, которые вы хотите отправить
    }

    # Отправляем данные в формате JSON
    return JsonResponse(data)

def ProductDetail(request, pk):
    products = Product.objects.filter(pk=pk)
    size = Size.objects.all()
    color = Color.objects.all()
    product_list = []
    for product in products:
        product_images = ProductImage.objects.filter(product=product)
        product_list.append({'product': product, 'product_images': product_images})

    context = {
        'product_list': product_list,
        'size':size,
        'color': color
    }
    return render(request, 'shop/product-detail.html', context)




def Corzina(request):
    return render(request, 'shop/shoping-cart.html')

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id) if size_id else None
        color = get_object_or_404(Color, id=color_id) if color_id else None

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        response_data = {
            'success': True,
            'product_id': product_id,
            'cart_count': cart.total_items,
        }
        return JsonResponse(response_data)
    return JsonResponse({'success': False}, status=400)


@login_required
@require_POST

def toggle_favorite(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if created:
        status = 'added'
    else:
        favorite.delete()
        status = 'removed'

    return JsonResponse({'status': status})
