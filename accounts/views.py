# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginTable, UserProfile 
from django.contrib.auth.hashers import make_password, check_password



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
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Get the user profile
            user_profile = UserProfile.objects.get(username=username)

            # Check if the password is correct
            if LoginTable.objects.filter(user_profile=user_profile).exists():
                login_table = LoginTable.objects.get(user_profile=user_profile)
                if password==login_table.password:
                    # Successful login logic here (e.g., setting session data)
                    messages.success(request, "Login successful!")
                    return redirect('adminhomepage',user_id=user_profile.id)
            if check_password(password, user_profile.password):
                # Successful login logic here (e.g., setting session data)
                messages.success(request, "Login successful!")
                
                return redirect('userhomepage',user_id=user_profile.id)
                  # Redirect to a home page or dashboard
            else:
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