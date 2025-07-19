from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    name = models.CharField(max_length=155, blank=False)
    mobile_number = models.CharField(max_length=10,blank=False,unique=True)

    def __str__(self):
        return self.username
