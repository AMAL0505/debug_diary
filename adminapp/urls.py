from django.urls import path
from . import views


urlpatterns = [
    path('adminhomepage/<int:user_id>/',views.adminHomePage,name='adminhomepage'),
    path('adminprofile/<int:user_id>/',views.adminProfile,name='adminprofile'),
]
