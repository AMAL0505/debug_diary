from django.urls import path
from . import views


urlpatterns = [
    path('adminhomepage/<int:user_id>/',views.adminHomePage,name='adminhomepage'),
]
