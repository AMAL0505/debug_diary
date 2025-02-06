from django.contrib import admin
from .models import UserProfile,LoginTable
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(LoginTable)