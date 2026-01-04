from django import forms

from shop_content.models import *
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'brand', 'gender', 'available_sizes', 'available_colors',
                  'date_added', 'availability', 'seasons', 'country', 'category']

class ImagesForms(forms.ModelForm):

    class Meta:
        model = ProductImage
        fields = ['image']

#brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

#Size
class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size_value']

#Colors
class ColorsForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['color_name']


#Country
class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


#Sesons

class SesonsForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name']

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slaider
        fields = ['img', 'subtext', 'main_text']

class AboutForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

