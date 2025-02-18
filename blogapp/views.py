from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Category, Notification,Comment
from accounts.models import UserProfile
from .forms import BlogForm
from django.contrib import messages

# Create your views here.



def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'blog/blog_list.html', {'blogs': blogs})


def blogDetailsPage(request,blog_id,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent__isnull=True).order_by('-created_at')
    context = {
        'blog':blog,
        'userprofile':userprofile,
        'comments':comments
    }
    return render(request, 'user/blog_details.html',context)


def filterBlogs(request, category_id, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    categories = Category.objects.all()
    blog_list = Blog.objects.filter(categories__id=category_id)  # Corrected for ManyToManyField

    context = {
        'blog_list': blog_list,
        'userprofile': userprofile,
        'categories': categories
    }
    return render(request, 'user/user_home.html', context)



def createBlog(request, user_id):
    userprofile = UserProfile.objects.get(id=user_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = userprofile  # Assign user
            blog.save()
            form.save_m2m()  # Save many-to-many categories
            return redirect('userhomepage',userprofile.id)  # Redirect after success
    else:
        form = BlogForm()

    return render(request, 'user/create_blog.html', {'form': form, 'userprofile': userprofile})


def viewAllBlogs(request):
    blogs = Blog.objects.all()
    return render(request,'admin/admin_view_all_blogs.html',{'blogs':blogs})


def userBlogs(request, user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=userprofile)
    return render(request, 'user/my_blogs.html', {'blogs': blogs, 'userprofile': userprofile})



def add_comment(request,blog_id,user_id):
    if request.method == "POST":
        user = get_object_or_404(UserProfile,id=user_id)
        comment_text = request.POST.get("comment")
        parent_id = request.POST.get("parent_id")

        blog = get_object_or_404(Blog, id=blog_id)
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        Comment.objects.create(
            user=user,
            blog=blog,
            comment=comment_text,
            parent=parent_comment
        )

        messages.success(request, "Comment added successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    messages.error(request, "Something went wrong!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

    

def like_comment(request,comment_id,user_id):
    if request.method == "POST":
        user = get_object_or_404(UserProfile,id=user_id)
        comment = get_object_or_404(Comment, id=comment_id)

        if user in comment.likes.all():
            comment.likes.remove(user)
            messages.info(request, "You unliked the comment.")
        else:
            comment.likes.add(user)
            messages.success(request, "You liked the comment!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    messages.error(request, "Invalid request.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def get_comments(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent=None).order_by("-created_at")

    return render(request, "blog_detail.html", {"blog": blog, "comments": comments})



def updateBlog(request, blog_id, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)  # Avoids "DoesNotExist" error

    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    print(f"Blog ID: {blog.id}, User ID: {userprofile.id}")
    if form.is_valid():
        form.save()
        return redirect('userblogs', user_id=user_id)  # Ensure 'userblogs' exists in urls.py

    return render(request, 'user/update_blog.html', {'form': form, 'userprofile': userprofile,'blog':blog})


def deleteBlog(request, blog_id,user_id):
    user = get_object_or_404(UserProfile,id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)  # Avoids "DoesNotExist" error
    blogs = Blog.objects.all()
    if request.method == 'POST':
        reason = request.POST.get('reason','no reason mentioned')
        Notification.objects.create(
            from_user=user,  # Assuming the admin is the user blocking the blog
            to_user=blog.user,  # The user who created the blog
            notification_type="POST_BLOCKED",
            message=f"Your blog '{blog.title}' has been deleted by the admin. Reason: {reason}",
        )
        blog.delete()
        messages.success(request, f"Blog '{blog.title}' has been deleted.")
        return render(request,'admin/admin_view_all_blogs.html',{'blogs':blogs})
    return redirect(request.META.get('HTTP_REFERER', '/'))


def blockBlog(request, blog_id,user_id):
    user = get_object_or_404(UserProfile,id =user_id)
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        # Get the reason for blocking from the form
        block_reason = request.POST.get('block_reason', 'No reason provided.')
        
        # Block the blog
        blog.is_published = False
        blog.is_blocked = True
        blog.save()
        
        # Create a notification for the user who authored the blog
        Notification.objects.create(
            from_user=user,  # Assuming the admin is the user blocking the blog
            to_user=blog.user,  # The user who created the blog
            blog=blog,  # Reference to the blocked blog
            notification_type="POST_BLOCKED",
            message=f"Your blog '{blog.title}' has been blocked by the admin. Reason: {block_reason}",
        )
        
        messages.success(request, f"Blog '{blog.title}' has been blocked.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def unBlockBlog(request,blog_id):
    blog = get_object_or_404(Blog,id=blog_id)
    blog.is_blocked = False
    blog.is_published = True
    blog.save()
    return redirect(request.META.get('HTTP_REFERER', '/')) 


def publishBlog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.is_published = True
    blog.save()

    return redirect(request.META.get('HTTP_REFERER', '/')) 


def pendingBlogs(request, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blogs = Blog.objects.filter(is_published=False, is_blocked=False)
    context = {
        'blogs': blogs,
        'userprofile': userprofile
    }
    return render(request, 'admin/admin_view_requests.html',context)
    


def blockedBlogs(request, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blogs = Blog.objects.filter(is_blocked=True)
    context = {
        'blogs': blogs,
        'userprofile': userprofile
    }
    return render(request, 'admin/admin_blocked_blogs.html',context)


def createNotification(request, from_user_id, to_user_id):
    from_user = get_object_or_404(UserProfile, id=from_user_id)
    to_user = get_object_or_404(UserProfile, id=to_user_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        notification = Notification(from_user=from_user, to_user=to_user, message=message)
        notification.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to previous page


def mark_all_notifications_read(request,user_id):
    """Marks all notifications as read"""
    user = get_object_or_404(UserProfile,id=user_id)
    Notification.objects.filter(to_user=user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def mark_notification_read(request, notification_id,user_id):
    """Marks a single notification as read"""
    user = get_object_or_404(UserProfile,id=user_id)
    Notification.objects.filter(id=notification_id, to_user=user).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))