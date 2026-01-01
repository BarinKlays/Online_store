from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.
from django.views import View
from django.contrib.auth import logout
from accounts.forms import RegisterForm
from accounts.models import UserInfo



def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'Вы успешно вошли в систему!!!!')
            login(request, user)
            # Redirect to a success page.
            if request.user.is_superuser:
                return redirect('adminka')
            else:
                return redirect('shopindex')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'error')
    return render(request, 'accounts/login.html')

def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            surname = form.cleaned_data['surname']
            phone_number = form.cleaned_data['phone_number']

            user_info = UserInfo.objects.create(
                user = user,
                surname = surname,
                phone_number = phone_number
            )

            user_info.save()

            if 'images' in request.FILES:
                user_info.images = request.FILES['images']
                user_info.save()

                login(request, user)
                return redirect('shopindex')
    else:
        form = RegisterForm()
        messages.error(request, "Найди ошибку!!!")
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('shopindex')

