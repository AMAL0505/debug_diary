# accounts/views.py
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from .models import LoginTable, UserProfile 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages



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






def userProfile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        return render(request, 'authentication/profile.html', {'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        messages.error(request, "User  not found.")
        return redirect('home')  # Redirect to a home page or error page



def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')





def userProfilePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    return render(request, 'user/user_profile.html',{'userprofile':userprofile})



def deleteUserProfile(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    userprofile.delete()
    return redirect('login')

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


def is_admin(user):
    try:
        userprofile = UserProfile.objects.get(username=user.username)  # Ensure we get the UserProfile instance
        login_entry = LoginTable.objects.get(user_profile=userprofile)
        return login_entry.type.lower() == "admin"  # Check if user is an admin
    except (UserProfile.DoesNotExist, LoginTable.DoesNotExist):
        return False  # Default to non-admin if no entry is found


def blockUser(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    # Check if the user is an admin
    login_entry = LoginTable.objects.filter(user_profile=user).first()
    
    if login_entry and login_entry.type.lower() == "admin":
        messages.error(request, "Admins cannot be blocked!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Block the user (non-admin)
    user.isblocked = True
    user.save()
    messages.success(request, f"User {user.username} has been blocked.")
    
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