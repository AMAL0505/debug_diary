from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/',views.userRegistration,name='register'),
    path('',views.userLogin,name='login'),
    path('userhomepage/<int:user_id>/',views.userHomePage,name='userhomepage'),
    path('userprofile/<int:user_id>/',views.userProfilePage,name='userprofile'),
    path('updateprofile/<int:user_id>/',views.updatUserProfile,name='updateprofile'),
    path('deleteprofile/<int:user_id>/',views.deleteUserProfile,name='deleteprofile'),
    
    path('adminhomepage/',views.adminHomePage,name='adminhomepage'),
    path('blogdetails/<int:user_id>/',views.blogDetailsPage,name='blogdetails'),
    path('logout/',views.logout_view,name='logout')
]

if settings.DEBUG:  # Only serve media in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)