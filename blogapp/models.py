from django.db import models
from accounts.models import UserProfile
from tinymce.models import HTMLField
from django.utils.timezone import now

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name



class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = HTMLField()
    categories = models.ManyToManyField(Category, related_name="blogs")
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.UserProfile',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment
    

class Notification(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_notifications")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Track if the user has seen it
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification from {self.from_user.username} to {self.to_user.username}"

