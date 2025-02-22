from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'user_type', 'email']

admin.site.register(CustomUser, UserModel)