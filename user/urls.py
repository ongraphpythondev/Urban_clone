from django.urls import path , include
from user import views

urlpatterns = [
    path('' , views.home , name = 'user'),
    path('login' , views.login , name = 'login'),
    path('register' , views.register , name = 'register'),
    path('logout' , views.logout , name = 'logout'),
    path('verify/<auth_token>' , views.verify , name = 'verify'),
    path('forget_password' , views.forget_password , name = 'forget_password'),
    path('reset_password/<auth_token>' , views.reset_password , name = 'reset_password'),
    path('category/<int:pk>' , views.category , name = 'category'),
    path('service/<int:servicepk>/<int:categorypk>' , views.service , name = 'service'),
    path('service/<int:servicepk>' , views.service , name = 'service'),
    path('addcart/<int:emp_pk>/<int:servicepk>/<int:categorypk>' , views.addcart , name = 'addcart'),
    path('addcart/<int:emp_pk>/<int:servicepk>' , views.addcart , name = 'addcart'),
    path('cart' , views.cart , name = 'cart'),
    path('order/<int:order_pk>' , views.order , name = 'order'),
    path('order/<int:order_pk>/<int:user_pk>' , views.order , name = 'order'),
    path('order' , views.order , name = 'order'),
    path('remove/<int:order_pk>' , views.remove , name = 'remove'),
    path('add_emp/<int:servicepk>/<int:categorypk>' , views.add_emp , name = 'add_emp'),
    path('add_emp/<int:servicepk>' , views.add_emp , name = 'add_emp'),
    path('checkout/<int:order_pk>' , views.checkout , name = 'checkout'),
    path('checkout/<int:order_pk>/<int:user_pk>' , views.checkout , name = 'checkout'),
    path('profile' , views.profile , name = 'profile'),
]