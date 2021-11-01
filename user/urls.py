from django.urls import path , include
from user import views

urlpatterns = [
    path('' , views.home , name = 'user'),
    path('login' , views.login , name = 'login'),
    path('register' , views.register , name = 'register'),
    path('logout' , views.logout , name = 'logout'),
    path('succes' , views.succes , name = 'succes'),
    path('error' , views.error , name = 'error'),
    path('verify/<auth_token>' , views.verify , name = 'verify'),
]