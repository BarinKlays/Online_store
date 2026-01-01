from .views import *
from django.urls import path

urlpatterns = [
    path('login/', Login, name='login'),
    path('register/', Register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),

]
