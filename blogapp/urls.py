from django.urls import path
from . import views

urlpatterns = [
    path('bloglist/',views.blog_list,name='bloglist'),
    path('blogdetails/<int:blog_id>/user/<int:user_id>/',views.blogDetailsPage,name='blogdetails'),
    path('filterblogs/<int:category_id>/user/<int:user_id>/',views.filterBlogs,name='filterblogs'),
    path('createblog/<int:user_id>/',views.createBlog,name='createblog'),
    path('userblogs/<int:user_id>/',views.userBlogs,name='userblogs'),
    path('viewallblogs/',views.viewAllBlogs,name='viewallblogs'),
    path('updateblog/<int:blog_id>/user/<int:user_id>/',views.updateBlog,name='updateblog'),
    path('deleteblog/<int:blog_id>/user/<int:user_id>/',views.deleteBlog,name='deleteblog'),
    path('blockblog/<int:blog_id>/user/<int:user_id>',views.blockBlog,name='blockblog'),
    path('unblockblog/<int:blog_id>',views.unBlockBlog,name='unblockblog'),
    path('publishblog/<int:blog_id>/',views.publishBlog,name='publishblog'),
    path('pendingblogs/<int:user_id>/',views.pendingBlogs,name='pendingblogs'),
    path('blockedblogs/<int:user_id>/',views.blockedBlogs,name='blockedblogs'),
    path("addcomment/<int:blog_id>/user/<int:user_id>/", views.add_comment, name="add_comment"),
    path("likecomment/<int:comment_id>/user/<int:user_id>/", views.like_comment, name="like_comment"),
    path("getcomments/<int:blog_id>/",views.get_comments,name="getcomments"),
    path('notifications/mark-all/<int:user_id>/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/mark/<int:notification_id>/user/<int:user_id>/', views.mark_notification_read, name='mark_notification_read'),
]
