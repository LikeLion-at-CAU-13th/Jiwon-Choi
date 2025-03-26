from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)

#model을 추가하면 꼭 admin에 추가해야 함