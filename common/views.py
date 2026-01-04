from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from accounts.models import *


from itertools import chain


# Create your views here.
from common.forms import *
from common.models import *
from shop_content.models import Slaider


def Adminka(request):
    total_products = Product.objects.count()
    total_users = User.objects.count()

    context = {
        'total_products': total_products,
        'total_users': total_users,
    }
    return render(request, 'common/index.html', context)

def DashBoard(request):
    return render(request, 'common/dashboard.html')

def AboutView(request):
    try:
        about = AboutUs.objects.get()
    except AboutUs.DoesNotExist:
        about = None

    context = {
        'about':about
    }

    return render(request, 'common/about.html', context)

def OrderHandler(request):
    user_baskets = Basket.objects.prefetch_related('cart__product')
    products = Product.objects.all()

    product_list = []
    for product in products:
        # Получаем изображения для текущего продукта
        product_images = ProductImage.objects.filter(product=product)
        # Добавляем информацию о продукте и его изображениях в список
        product_list.append({
            'product': product,
            'images': product_images  # Передаем список изображений для каждого продукта
        })
    for basket in user_baskets:
        for item in basket.cart.all():
            print(f"CartItem: {item}, Product: {item.product if item.product else 'None'}")
        print(basket.cart.all)
        basket.save()  # Сохранение изменений в корзине

    context = {
        'basket': user_baskets,
        'product_list': product_list,
    }
    print(Basket.objects.filter(user=request.user).first())
    return render(request, 'common/orderhandler.html', context)

def UpladedOrder(request, pk):
    order = get_object_or_404(Basket, pk=pk)
    if request.method == 'POST':
        order.status = 'Search'
        order.save()
    return redirect('orderhandler')

def YpokovOrder(request, pk):
    order = get_object_or_404(Basket, pk=pk)
    if request.method == 'POST':
        order.status = 'Ypokov'
        order.save()
    return redirect('orderhandler')

def OtpravkaOrder(request, pk):
    order = get_object_or_404(Basket, pk=pk)
    if request.method == 'POST':
        order.status = 'Otpravka'
        order.save()
    return redirect('orderhandler')

def CompletedOrder(request, pk):
    order = get_object_or_404(Basket, pk=pk)
    if request.method == 'POST':
        order.status = 'Completed'
        order.save()
    return redirect('orderhandler')




def EditAbout(request):
    about = AboutUs.objects.first()
    if request.method =="POST":
        editform = AboutForm(request.POST, request.FILES, instance=about)
        if editform.is_valid():
            editform.save()

            return redirect('aboutview')
    else:
        editform = AboutForm(instance=about)

    context = {
        'editform':editform
    }

    return render(request, 'common/editabout.html', context)

def ContactView(request):
    contact = Contact.objects.get()


    context = {
        'contact':contact
    }

    return render(request, 'common/contact.html', context)

def EditContact(request):
    contact = Contact.objects.first()
    if request.method =="POST":
        editform = ContactForm(request.POST, request.FILES, instance=contact)
        if editform.is_valid():
            editform.save()

            return redirect('contactviewadmin')
    else:
        editform = ContactForm(instance=contact)

    context = {
        'editform':editform
    }

    return render(request, 'common/editcontact.html', context)


#slider

def Slider(request):
    slider = Slaider.objects.all()

    context = {
        'slider':slider
    }

    return render(request, 'common/slider/sliderview.html', context)

def AddSlider(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return render('slider')

    else:
        form =SliderForm()

    context = {
        'form':form
    }
    return render(request,'common/slider/addslider.html', context)

def EditSlider(request, pk):
    slider = get_object_or_404(Slaider, pk=pk)
    if request.method =="POST":
        editform = SliderForm(request.POST, request.FILES, instance=slider)
        if editform.is_valid():
            editform.save()

            return redirect('slider')
    else:
        editform = SliderForm(instance=slider)

    context = {
        'editform':editform
    }

    return render(request, 'common/slider/editslider.html', context)

def DeleteSlider(request, pk):
    slider = get_object_or_404(Slaider, pk=pk)
    slider.delete()
    return redirect('slider')


def FeedBackview(requset):
    feedback = FeedBack.objects.all()

    context = {
        'feedback':feedback
    }

    return render(requset, 'common/feedback.html', context)

def AddSliderView(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slider')

    else:
        form = SliderForm()

    context = {
        'form': form
    }
    return render(request, 'common/slider/addslider.html', context)


# Продукты

def ProductList(request):
    products = Product.objects.all()

    product_list = []
    for item in products:
        productsimage = ProductImage.objects.filter(product__pk=item.pk)
        product_list.append({'productimage': productsimage, 'info': item})
        print(product_list)

    # products_one = Product.objects.get(pk=1)
    context = {"product_list" : product_list,
               }
    return render(request, 'common/product_list.html', context)


def AddProduct(request):
    brand = Brand.objects.all()
    size = Size.objects.all()
    colors = Color.objects.all()
    country = Country.objects.all()
    sesons = Season.objects.all()
    category = Category.objects.all()
    product_gender = Product.GENDER
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        images_form = ImagesForms(request.POST, request.FILES)

        if product_form.is_valid() and images_form.is_valid():
            product = product_form.save(commit=False)  # Сохраняем основную информацию о продукте

            # Получаем ID выбранной категории из данных формы
            category_id = request.POST.get('category')

            # Устанавливаем ID категории в поле category_id объекта Product
            product.category_id = category_id

            product.save()

            # Получаем список загруженных файлов из формы изображений
            images = request.FILES.getlist('image')

            # Проходимся по каждому файлу и создаем запись ProductImage
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('product_list')

    else:
        product_form = ProductForm()
        images_form = ImagesForms()

    context =  {
        'product_form':product_form,
        'images_form':images_form,
        'brand':brand,
        'size':size,
        'colors': colors,
        'country': country,
        'sesons':sesons,
        'product_gender':product_gender,
        'category':category,
    }
    print(product_form),
    print(images_form),
    return render(request, 'common/add_product.html', context)


def ProductEdit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    ImageFormSet = modelformset_factory(ProductImage, form=ImagesForms, extra=5, max_num=5)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()

            ProductImage.objects.filter(product=product).delete()

            for form in formset:
                if form.is_valid() and form.cleaned_data.get('image'):
                    ProductImage.objects.create(product=product, image=form.cleaned_data['image'])

            return redirect('product_list')

    else:
        product_form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=ProductImage.objects.filter(product=product))
    context = {
        'product_form': product_form,
        'formset': formset
    }



    return render(request, 'common/product_edit.html', context)


def Product_detail(request, pk):
    products = Product.objects.filter(pk=pk)

    product_list = []
    for product in products:
        product_images = ProductImage.objects.filter(product=product)
        product_list.append({'product': product, 'product_images': product_images})

    context = {
        'product_list': product_list,
    }


    return render(request, 'common/product_detail.html', context)

def Delete_Product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

class UserList(View):
    def get(self, request):

        user = User.objects.all()

        users_list = []
        for item in user:
            try:
                userinfo = UserInfo.objects.get(user__pk=item.pk)
                users_list.append({'info': userinfo, 'username': item})
            except UserInfo.DoesNotExist:
                users_list.append({'info': '0', 'username': item})
        print(users_list)

        contex = {
            'users_list': users_list,
        }

        return render(request, 'common/user_list.html', contex)

# Характеристики

#brand
def Brand_view(request):
    brand = Brand.objects.all()

    context = {
        'brand': brand
    }
    return render(request, 'common/brand.html', context)

def AddBrand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand')
    else:

        form = BrandForm()
    context = {
        'form': form
    }

    return render(request, 'common/add_brand.html', context)

def EditBrand(request, pk):
    editbrend = get_object_or_404(Brand, pk=pk)

    if request.method =="POST":
        editform = BrandForm(request.POST, instance=editbrend)
        if editform.is_valid():
            editform.save()

            return redirect('brand')
    else:
        editform = BrandForm(instance=editbrend)

    context = {
        'editform':editform
    }

    return render(request, 'common/edit_brend.html', context)

def DeleteBrand(request, pk):
    delete_brand = get_object_or_404(Brand, pk=pk)
    delete_brand.delete()
    return redirect('brand')



# size

def Size_view(request):
    size = Size.objects.all()

    context = {
        'size': size
    }
    return render(request, 'common/size.html', context)

def Add_Size(request):
    if request.method == "POST":
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('size')
    else:

        form = SizeForm()
    context = {
        'form': form
    }
    return render(request, 'common/add_Size.html', context)

def Edit_Size(request, pk):
    name = get_object_or_404(Size, pk=pk)
    if request.method == 'POST':
        form = SizeForm(request.POST, instance=name)
        if form.is_valid():
            form.save()
            return redirect('size')
    else:
        form = SizeForm(request.POST, instance=name)
    context = {
        'form': form
    }

    return render(request, 'common/edit_size.html', context)

def DeleteSize(request, pk):
    size = get_object_or_404(Size, pk=pk)
    size.delete()
    return redirect('size')

# color
def Colors_view(request):
    color = Color.objects.all()

    context = {
        'color': color
    }
    return render(request, 'common/colors.html', context)

def AddColors(request):
    if request.method == "POST":
        form = ColorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('colors')
    else:
        form = ColorsForm()

    context = {
        'form': form
    }

    return render(request, 'common/add_colors.html', context)

def ColorsEdit(request, pk):
    color = get_object_or_404(Color, pk=pk)
    if request.method == "POST":
        form = ColorsForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return redirect('colors')

    else:
        form = ColorsForm(instance=color)
    context = {
        'form':form
    }

    return render(request, 'common/edit_colors.html', context)

def DeleteColors(request, pk):
    color = get_object_or_404(Color, pk=pk)
    color.delete()
    return redirect('colors')

# sesons

def Sesons_view(request):
    sesons = Season.objects.all()

    context = {
        'sesons': sesons
    }
    return render(request, 'common/sesons.html', context)

def AddSesons(request):
    if request.method == "POST":
        form = SesonsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sesons')
    else:
        form = SesonsForm()

    context = {
        'form': form
    }

    return render(request, 'common/add_sesons.html', context)

def SesonsEdit(request, pk):
    sesons = get_object_or_404(Season, pk=pk)
    if request.method == "POST":
        form = SesonsForm(request.POST, instance=sesons)
        if form.is_valid():
            form.save()
            return redirect('sesons')

    else:
        form = SesonsForm(instance=sesons)
    context = {
        'form':form
    }

    return render(request, 'common/edit_sesons.html', context)

def DeleteSesons(request, pk):
    sesons = get_object_or_404(Season, pk=pk)
    sesons.delete()
    return redirect('sesons')

# Country

def Country_view(request):
    country = Country.objects.all()

    context = {
        'country': country
    }
    return render(request, 'common/country.html', context)

def AddCountry(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('country')
    else:
        form = CountryForm()

    context = {
        'form': form
    }

    return render(request, 'common/add_country.html', context)

def CountryEdit(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('country')

    else:
        form = CountryForm(instance=country)
    context = {
        'form':form
    }

    return render(request, 'common/edit_country.html', context)

def DeleteCountry(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return redirect('country')