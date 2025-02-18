# accounts/views.py
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages

from blogapp.models import Notification
from .models import LoginTable, UserProfile 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import logout



def userRegistration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        ph_no = request.POST['ph_no']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        profile_pic = request.FILES.get('profile_pic')  # Get the uploaded file

        if password == cpassword:
            # Check if the username already exists
            if not UserProfile.objects.filter(username=username).exists():
                # Hash the password before storing
                hashed_password = make_password(password)

                # Create UserProfile
                user_profile = UserProfile.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    ph_no=ph_no,
                    password=hashed_password,  # Store hashed password
                    profile_pic=profile_pic  # Store the uploaded profile picture
                )

                # Store in LoginTable
                print("Creating LoginTable entry for:", username)
                LoginTable.objects.create(
                    user_profile=user_profile,  # Link to UserProfile
                    first_name=first_name,
                    last_name=last_name,
                    password=hashed_password,  # Store hashed password
                    type='user'
                )

                messages.success(request, "Registration successful! Please log in.")
                print("Created LoginTable entry for:", username)
                return redirect('login')
            else:
                messages.error(request, "Username already exists.")
                return redirect('register')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

    return render(request, 'accounts/authentication.html')


def userLogin(request):
    print("function called") 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Get the user profile
            user_profile = UserProfile.objects.get(username=username)

            # Debugging: Print user profile ID
            print(f"User Profile ID: {user_profile.id}")

            # Check if user is blocked
            if user_profile.isblocked:
                messages.error(request, "Your account is blocked.")
                return redirect('login')

            # Check login credentials in LoginTable
            login_table = LoginTable.objects.filter(user_profile=user_profile).first()
            if login_table and password == login_table.password:
                request.session['user_id'] = user_profile.id  # ✅ Store user_id in session
                
                # Debugging: Print session data
                print(f"Session Data: {request.session.get('user_id')}")

                messages.success(request, "Login successful!")
                return redirect('adminhomepage', user_id=user_profile.id)

            # Check password directly from UserProfile (if applicable)
            if check_password(password, user_profile.password): 
                request.session['user_id'] = user_profile.id  # ✅ Store user_id in session
                
                # Debugging: Print session data
                print(f"Session Data: {request.session.get('user_id')}")

                messages.success(request, "Login successful!")
                return redirect('userhomepage', user_id=user_profile.id)

            messages.error(request, "Invalid username or password.")
            return redirect('login')

        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/authentication.html')



def forgot_password(request):
    print("forgot password function called")
    
    # Clear old messages to prevent persistence
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        print("checking condition")
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            print("checking passwords condition")
            try:
                userprofile = get_object_or_404(UserProfile, email=email)
                userprofile.password = make_password(password)
                userprofile.save()
                messages.success(request, "Password reset successful! Please log in with your new password.")
                return redirect('login')
            except:
                messages.error(request, "Account doesn't exist with the given email")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'accounts/forgot_password.html')




def userProfile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        return render(request, 'authentication/profile.html', {'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        messages.error(request, "User  not found.")
        return redirect('home')  # Redirect to a home page or error page





def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully.")  # Show logout message
    return redirect('login')  





def userProfilePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    return render(request, 'user/user_profile.html',{'userprofile':userprofile})



def deleteUserProfile(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    userprofile.delete()
    return redirect('login')



def updatUserProfile(request,user_id):
    print("function called")
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
        userprofile.profile_pic = request.FILES['profile_pic']
        userprofile.save()
        logintable.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))  

def updateProfilePic(request,user_id):
    print("function called")
    userprofile = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        userprofile.profile_pic = request.FILES.get('profile_pic')
        userprofile.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))  

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


def is_admin(user):
    try:
        userprofile = UserProfile.objects.get(username=user.username)  # Ensure we get the UserProfile instance
        login_entry = LoginTable.objects.get(user_profile=userprofile)
        return login_entry.type.lower() == "admin"  # Check if user is an admin
    except (UserProfile.DoesNotExist, LoginTable.DoesNotExist):
        return False  # Default to non-admin if no entry is found


def blockUser (request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    login_entry = LoginTable.objects.filter(user_profile=user).first()
    
    if request.method == 'POST':
        if login_entry and login_entry.type.lower() == "admin":
            messages.error(request, "Admins cannot be blocked!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        # Toggle block status
        user.isblocked = not user.isblocked
        user.save()
        
        if user.isblocked:
            message = "Your account has been blocked by the admin."
            Notification.objects.create(
                from_user=user,
                to_user=user,
                notification_type="ACCOUNT_BLOCKED",
                message=message,
            )
            messages.success(request, f"User  {user.username} has been blocked.")
        else:
            messages.success(request, f"User  {user.username} has been unblocked.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def blockedUsers(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blocked_users = UserProfile.objects.filter(isblocked=True)
    context = {
        'userprofile':userprofile,
        'blocked_users':blocked_users}
    return render(request, 'admin/admin_blocked_users.html', context)


def unblockUser(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.isblocked = False
    user.save()
    messages.success(request, f"User {user.username} has been unblocked.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def availableUsers(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    available_users = LoginTable.objects.filter(type='user',user_profile__isblocked=False)
    context = {
        'userprofile':userprofile,
        'available_users':available_users
    }

    return render(request, 'admin/admin_user_list.html', context)


def allUsers(request):
    user_list = LoginTable.objects.all()
    return render(request,'admin/admin_view_all_user.html',{'user_list':user_list})