from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/',views.userRegistration,name='register'),
    path('',views.userLogin,name='login'),
    path('deleteprofile/<int:user_id>/',views.deleteUserProfile,name='deleteprofile'),
    path('forgotpassword/',views.forgot_password,name='forgotpassword'),
    path('blockuser/<int:user_id>/',views.blockUser,name='blockuser'),
    path('logout/',views.logout_view,name='logout'),
    path('blockedusers/<int:user_id>',views.blockedUsers,name='blockedusers'),
    path('unblockuser/<int:user_id>/',views.unblockUser,name='unblockuser'),
    path('updateprofile/<int:user_id>/',views.updatUserProfile,name='updateprofile'),
    path('updateprofilepic/<int:user_id>/',views.updateProfilePic,name='updateprofilepic'),
    path('availableusers/<int:user_id>/',views.availableUsers,name='availableusers'),
    path('allusers/',views.allUsers,name='allusers')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)