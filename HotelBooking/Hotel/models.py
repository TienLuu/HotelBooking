from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime
import json

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to="user/avatar/%Y/%m/%D/")
