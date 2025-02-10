from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/',views.userRegistration,name='register'),
    path('',views.userLogin,name='login'),
    path('deleteprofile/<int:user_id>/',views.deleteUserProfile,name='deleteprofile'),
    path('blockuser/<int:user_id>/',views.blockUser,name='blockuser'),
    path('logout/',views.logout_view,name='logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)