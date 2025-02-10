from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Category
from accounts.models import UserProfile
from .forms import BlogForm

# Create your views here.



def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'blog/blog_list.html', {'blogs': blogs})


def blogDetailsPage(request,blog_id,user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blog = Blog.objects.get(id=blog_id)
    context = {
        'blog':blog,
        'userprofile':userprofile
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


def userBlogs(request, user_id):
    userprofile = UserProfile.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=userprofile)
    return render(request, 'user/my_blogs.html', {'blogs': blogs, 'userprofile': userprofile})


def updateBlog(request, blog_id, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)  # Avoids "DoesNotExist" error

    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    print(f"Blog ID: {blog.id}, User ID: {userprofile.id}")
    if form.is_valid():
        form.save()
        return redirect('userblogs', user_id=user_id)  # Ensure 'userblogs' exists in urls.py

    return render(request, 'user/update_blog.html', {'form': form, 'userprofile': userprofile,'blog':blog})


def deleteBlog(request, blog_id, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)  # Avoids "DoesNotExist" error

    if request.method == 'POST':
        blog.delete()
        return redirect('userblogs', user_id=user_id)

    return render(request, 'user/my_blogs.html', {'blog': blog, 'userprofile': userprofile})


def publishBlog(request, blog_id, user_id):
    userprofile = get_object_or_404(UserProfile, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id)

    blog.is_published = True
    blog.save()

    return redirect(request.META.get('HTTP_REFERER', '/')) 

    
