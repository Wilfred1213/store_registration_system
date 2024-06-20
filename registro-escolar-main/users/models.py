from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    administrador = models.BooleanField(default = False)
    profesor=models.BooleanField(default = False)
    digitador=models.BooleanField(default = False)

