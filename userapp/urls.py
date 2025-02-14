from django.urls import path
from . import views

urlpatterns = [
     path('userhomepage/<int:user_id>/',views.userHomePage,name='userhomepage'),
     path('userprofile/<int:user_id>/',views.userProfilePage,name='userprofile'),
]
