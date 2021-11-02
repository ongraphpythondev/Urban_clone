from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from user.models import Profile , Services , Categorys , Employee , Choose 
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.
# mpmgmaelbrobpysy
def home(req):
    services = Services.objects.all()
    print(services)
    return render(req, 'user/home.html' , {"services" : services})

def login(req):
    if req.method == "GET":
        return render(req, "user/login.html")
    elif req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']

        # it checks username presine in User 
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(req, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj ).first()
        # it check the user is email verified or not
        if not profile_obj.is_verified:
            messages.success(req, 'Profile is not verified check your mail.')
            return redirect('/login')

        # it check the username and password 
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


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def logout(req):
    auth.logout(req)
    return redirect('/')

def succes(req):
    return render(req , 'succes.html')

def error(request):
    return  render(request , 'error.html')


def forget_password(req):
    if req.method == "GET":
        return render(req, "user/forget_password.html")

    elif req.method == 'POST':
        email = req.POST.get('email')

        try:
            user_obj = User.objects.filter(email = email).first()
            if user_obj is None:
                messages.success(req, 'User not found.')
                return redirect('/forget_password')
            
            
            profile_obj = Profile.objects.filter(user = user_obj).first()
            auth_token = profile_obj.auth_token
            send_mail_for_reset_password(email , auth_token)
            return render(req, "user/succes.html")

        except Exception as e:
            print(e)

def send_mail_for_reset_password(email , token):
    subject = 'Your accounts need to reset password'
    message = f'Hi paste the link to reset the password http://127.0.0.1:8000/reset_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def reset_password(req , auth_token):
    if req.method == "GET":
        return render(req, "user/reset_password.html")

    elif req.method == 'POST':
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(req, 'Password and confirm password are different.')
            return redirect('/reset_password')

        try:
            profile_obj = Profile.objects.filter(auth_token = auth_token).first()

            if profile_obj:
                username = profile_obj.user.username
                user_obj = User.objects.filter(username = username).first()
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, 'Your password is changed.')
                return redirect('/login')
            else:
                return redirect('/error')
        except Exception as e:
            print(e)
            return redirect('/')


def category(req, pk):
    ser_obj = Services.objects.filter(pk = pk).first()
    if not ser_obj.sub_category:
        return redirect(f'/service/{ser_obj.id}')
    
    cat_obj = Categorys.objects.filter(service = ser_obj.service)
    return render(req , 'user/category.html' , {"categorys":cat_obj , 'serviceid': ser_obj.id})
        
        
        
def service(req ,servicepk, categorypk = None):
    print(categorypk)
    ser_obj = Services.objects.filter(pk = servicepk).first()
    if categorypk is None:
        emp_obj = Employee.objects.filter(service = ser_obj.service).all()
    else:
        cat_obj = Categorys.objects.filter(pk = categorypk).first()
        emp_obj = Employee.objects.filter(category = cat_obj.category).all()
    print(emp_obj)
    return render(req , 'user/service.html' , {'employees' : emp_obj , 'servicepk':servicepk , 'categorypk' : categorypk})


@login_required(login_url='/login')
def addcart(req , emp_pk ,servicepk, categorypk):
    user_obj = req.user
    choose_obj = Choose.objects.create(user_id = user_obj.id , emp_id= emp_pk , cart = True , )
    choose_obj.save()
    messages.success(req, 'Your service is added to cart .')
    return redirect(f'/service/{servicepk}/{categorypk}')


@login_required(login_url='/login')
def cart(req):
    emplist = []
    user_obj = req.user
    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = True , ).all()
    for emp in choose_obj:
        emplist.append(Employee.objects.filter(pk = emp.emp_id).all() )
    
    print(emplist[1][0])
    return render(req , 'user/cart.html' , {'orders' : emplist })

