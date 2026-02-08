from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=300, blank=True)
    phone_number = models.CharField(max_length=300, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # use email instead of username
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email