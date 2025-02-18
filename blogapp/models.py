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
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('accounts.UserProfile', related_name="liked_comments", blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return self.comment[:50]  # Return first 50 characters for better readability

    @property
    def like_count(self):
        return self.likes.count()

    

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("ACCOUNT_BLOCKED", "Account Blocked"),
        ("POST_BLOCKED", "Post Blocked"),
        ("GENERAL_ALERT", "General Alert"),
    ]

    from_user = models.ForeignKey(  
        UserProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name="sent_notifications"
    )  # Admin who sent the notification
    to_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_notifications"
    )
    blog = models.ForeignKey(  
        Blog, null=True, blank=True, on_delete=models.CASCADE, related_name="user_notifications"
    )  # Used only when blocking a post
    message = models.TextField()  # Message will now contain the reason
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="GENERAL_ALERT")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = self.from_user.username if self.from_user else "Admin"
        if self.notification_type == "POST_BLOCKED":
            return f"Post Blocked by {sender}: {self.to_user.username}'s post '{self.blog.title}'"
        elif self.notification_type == "ACCOUNT_BLOCKED":
            return f"Account Blocked by {sender}: {self.to_user.username}"
        return f"Notification ({self.notification_type}) from {sender} to {self.to_user.username}"


