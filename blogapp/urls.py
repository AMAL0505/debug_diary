from django.urls import path
from . import views

urlpatterns = [
    path('bloglist/',views.blog_list,name='bloglist'),
    path('blogdetails/<int:blog_id>/user/<int:user_id>/',views.blogDetailsPage,name='blogdetails'),
    path('filterblogs/<int:category_id>/user/<int:user_id>/',views.filterBlogs,name='filterblogs'),
    path('createblog/<int:user_id>/',views.createBlog,name='createblog'),
    path('userblogs/<int:user_id>/',views.userBlogs,name='userblogs'),
    path('updateblog/<int:blog_id>/user/<int:user_id>/',views.updateBlog,name='updateblog'),
    path('deleteblog/<int:blog_id>/user/<int:user_id>/',views.deleteBlog,name='deleteblog'),
    path('publishblog/<int:blog_id>/user/<int:user_id>/',views.publishBlog,name='publishblog'),
]
