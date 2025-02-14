from django.shortcuts import render,redirect
from accounts.models import LoginTable, UserProfile 
from blogapp.models import Blog, Category
from django.contrib.auth.hashers import make_password

# Create your views here.

def userHomePage(request,user_id):
    blog_list = Blog.objects.filter(is_published=True)
    categories = Category.objects.all()
    context = {'blog_list':blog_list,'categories':categories}
    return render(request, 'user/user_home.html',context)

def userProfilePage(request,user_id):
    return render(request, 'user/user_profile.html')





def updateProfilePic(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        userprofile.profile_pic = request.FILES.get('profile_pic')
        userprofile.save()
        return redirect('userprofile',user_id=user_id)
    return render(request, 'user/update_profile_pic.html',{'userprofile':userprofile})



def changePassword(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            userprofile.password = make_password(password)
            userprofile.save()
            return redirect('userprofile',user_id=user_id)
    return render(request, 'user/change_password.html',{'userprofile':userprofile})

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')
