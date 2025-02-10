from django.shortcuts import render
from accounts.models import UserProfile

# Create your views here.


def adminHomePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    return render(request, 'admin/admin_home.html',{'userprofile':userprofile})