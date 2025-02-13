from django.urls import path
from . import views


urlpatterns = [
    path('adminhomepage/<int:user_id>/',views.adminHomePage,name='adminhomepage'),
    path('adminprofile/<int:user_id>/',views.adminProfile,name='adminprofile'),
    path('adminblogdetails/<int:blog_id>/user/<int:user_id>',views.adminBlogDetails,name='adminblogdetails'),
]
