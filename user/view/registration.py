from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# register page
def register(request):
    
    # it check user login with admin account 
    if request.user.is_authenticated:
        user_obj = request.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')
        return redirect('/')


    if request.method == "GET":
        return render(request, "user/register.html")

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # checking all data 
        if not username:
            messages.error(request, 'Please fill username.')
            return render(request, "user/register.html")
        elif len(username) < 4:
            messages.error(request, 'Username length must be greater than 4 letter.')
            return render(request, "user/register.html")
        elif not email:
            messages.error(request, 'Please fill email.')
            return render(request, "user/register.html")
        elif len(email) < 5:
            messages.error(request, 'Email length must be greater than 4 letter.')
            return render(request, "user/register.html")
        elif not address:
            messages.error(request, 'Please fill address.')
            return render(request, "user/register.html")
        elif not password:
            messages.error(request, 'Please fill password.')
            return render(request, "user/register.html")
        elif len(password) < 6:
            messages.error(request, 'Password must greater than 6 character')
            return render(request, "user/register.html")

        try:
            # it check username is already taken or not
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return render(request, "user/register.html")

            # it check email is already taken or not
            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return render(request, "user/register.html")
            
            # creating user
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            print('this is user obj')
            # creating profile of user
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token , address=address)
            profile_obj.save()
            print('this is profile obj')
            # send mail to user for authenticate 
            send_mail_after_registration(email , auth_token)
            messages.success(request, 'Email sended to user plese check.')
            return redirect("/login")

        except Exception as e:
            print(e)

# it send email to user with token
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://localhost:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
