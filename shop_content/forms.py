from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from shop_content.models import *
from django import forms


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = '__all__'


class SubForm(forms.ModelForm):
    class Meta:
        model = Sub
        fields = '__all__'

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if email.split('.')[-1] != 'edu':
                raise forms.ValidationError("Only .edu email addresses allowed")
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("User with that email already exists")
            return email

class EidtRegisterForm(UserChangeForm):
    surname = forms.CharField(max_length=255)
    phone_number = forms.IntegerField()
    images = forms.ImageField()
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'surname', 'email', 'phone_number', 'images' ]


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['country_basket', 'state', 'postcode']