from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=200, unique=True)  # Ensure usernames are unique
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    ph_no = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    isblocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class LoginTable(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Link to UserProfile
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.user_profile.username  # Return the username from the related UserProfile