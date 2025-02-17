from django.shortcuts import render
from accounts.models import UserProfile,LoginTable
from blogapp.models import Blog, Comment

# Create your views here.


def adminHomePage(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blocked_users = UserProfile.objects.filter(isblocked=True).count()
    blog_list = Blog.objects.filter(is_published=False)
    unpublished_percentage = getblog_percentage()
    blog_count = Blog.objects.count(),
    user_count = LoginTable.objects.filter(type='user').count()
    pending_blog_count = Blog.objects.filter(is_published=False).count()
    context = {
        'userprofile':userprofile,
        'blog_list':blog_list,
        'blocked_users':blocked_users,
        'unpublished_percentage':unpublished_percentage,
        'blog_count':blog_count,
        'user_count':user_count,
        'pending_blog_count':pending_blog_count
    }
    return render(request, 'admin/admin_home.html',context)

def getblog_percentage():
    total_blogs = Blog.objects.count()
    published_blogs = Blog.objects.filter(is_published=True).count()

    if total_blogs == 0:
        return 0  # Avoid division by zero

    percentage = (published_blogs / total_blogs) * 100
    return round(percentage, 2)  # Round to 2 decimal places


def adminProfile(request,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    context = {
        'userprofile':userprofile
    }
    return render(request, 'admin/admin_profile.html',context)


def adminBlogDetails(request,blog_id,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent__isnull=True).order_by('-created_at')
    context = {
        'userprofile':userprofile,
        'blog':blog,
        'comments':comments
    }
    return render(request, 'admin/admin_blog_details.html',context)