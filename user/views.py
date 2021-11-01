from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from user.models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
# mpmgmaelbrobpysy
def home(req):
    return render(req, 'user/home.html')

def login(req):
    if req.method == "GET":
        return render(req, "user/login.html")
    elif req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        # it will add to User model
        user = auth.authenticate(username = username , password = password)
        if user is not None:

            auth.login(req , user)
            messages.success(req , 'user login successfully')
            return redirect('/')
        else:
            messages.info(req , 'invalid cridenctial')

    return render(req , 'user/login.html' )

def register(request):

    if request.method == "GET":
        return render(request, "user/register.html")

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                # return redirect('/register')
                return render(request, "user/register.html")

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                # return redirect('/register')
                return render(request, "user/register.html")
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            # return redirect('/succes')
            return render(request, "user/succes.html")

        except Exception as e:
            print(e)

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def logout(req):
    auth.logout(req)
    return redirect('/')

def succes(req):
    return render(req , 'succes.html')

def error(request):
    return  render(request , 'error.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )