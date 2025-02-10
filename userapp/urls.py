from django.urls import path
from . import views

urlpatterns = [
     path('userhomepage/<int:user_id>/',views.userHomePage,name='userhomepage'),
     path('userprofile/<int:user_id>/',views.userProfilePage,name='userprofile'),
     path('updateprofile/<int:user_id>/',views.updatUserProfile,name='updateprofile'),
     path('logout/',views.logout_view,name='logout')
]
