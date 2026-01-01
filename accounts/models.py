from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    images = models.ImageField(upload_to='avatars/', blank=False)
    datatime = models.DateTimeField(default=timezone.now)



    class Meta:
        app_label = 'accounts'