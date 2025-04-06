from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
#지금 당장은 새로운 필드를 추가하지 않을 예정이라 pass로 둠
