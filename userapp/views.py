from django.shortcuts import render,redirect
from accounts.models import LoginTable, UserProfile 
from blogapp.models import Blog, Category

# Create your views here.

def userHomePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blog_list = Blog.objects.all()
    categories = Category.objects.all()
    context = {'userprofile':userprofile,'blog_list':blog_list,'categories':categories}
    return render(request, 'user/user_home.html',context)

def userProfilePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    return render(request, 'user/user_profile.html',{'userprofile':userprofile})


def updatUserProfile(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    logintable = LoginTable.objects.get(user_profile=userprofile)
    if request.method == 'POST':
        userprofile.username = request.POST['username']
        userprofile.first_name = request.POST['first_name']
        logintable.first_name = request.POST['first_name']
        userprofile.last_name = request.POST['last_name']
        logintable.last_name = request.POST['last_name']
        userprofile.email = request.POST['email']  
        userprofile.ph_no = request.POST['ph_no']
        userprofile.save()
        logintable.save()
        return redirect('userprofile',user_id=user_id)
    return render(request, 'user/user_profile.html',{'userprofile':userprofile})


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
