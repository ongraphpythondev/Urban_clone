from django.urls import path , include
from user import views
from user.view.login import login
from user.view.registration import register
from user.view.logout import logout
from user.view.forget_password import verify
from user.view.forget_password import forget_password
from user.view.forget_password import reset_password
from user.view.service import category
from user.view.service import service
from user.view.cart import addcart
from user.view.cart import cart
from user.view.order import order
from user.view.cart import remove
from user.view.employee import add_emp
from user.view.checkout import checkout
from user.view.profile import profile
from user.view.order import cancel_order
from user.view.notification import notification
from user.view.notification import decline
from user.view.notification import accept
from user.view.update import update

urlpatterns = [
    path('' , views.home , name = 'user'),
    path('login/' , login , name = 'login'),
    path('register' , register , name = 'register'),
    path('logout' , logout , name = 'logout'),
    path('verify/<auth_token>' , verify , name = 'verify'),
    path('forget_password' , forget_password , name = 'forget_password'),
    path('reset_password/<auth_token>' , reset_password , name = 'reset_password'),
    path('category/<int:pk>' , category , name = 'category'),
    path('service/<int:servicepk>/<int:categorypk>' , service , name = 'service'),
    path('service/<int:servicepk>' , service , name = 'service'),
    path('addcart/<int:emp_pk>/<int:servicepk>/<int:categorypk>' , addcart , name = 'addcart'),
    path('addcart/<int:emp_pk>/<int:servicepk>' , addcart , name = 'addcart'),
    path('cart' , cart , name = 'cart'),
    path('order/<int:order_pk>' , order , name = 'order'),
    path('order/<int:order_pk>/<int:user_pk>' , order , name = 'order'),
    path('order' , order , name = 'order'),
    path('remove/<int:order_pk>' , remove , name = 'remove'),
    path('add_emp/<int:servicepk>/<int:categorypk>' , add_emp , name = 'add_emp'),
    path('add_emp/<int:servicepk>' , add_emp , name = 'add_emp'),
    path('checkout/<int:order_pk>' , checkout , name = 'checkout'),
    path('checkout/<int:order_pk>/<int:user_pk>' , checkout , name = 'checkout'),
    path('profile/' , profile , name = 'profile'),
    path('cancel_order/<int:order_pk>' , cancel_order , name = 'cancel_order'),
    path('notification' , notification , name = 'notification'),
    path('decline/<int:order_pk>' , decline , name = 'decline'),
    path('accept/<int:order_pk>' , accept , name = 'accept'),
    path('update' , update , name = 'update'),
    
]