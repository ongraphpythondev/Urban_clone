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

# home page
def home(req):
    services = Services.objects.all()
    return render(req, 'user/home.html' , {"services" : services})

# login page
def login(req):
    if req.user.is_authenticated:
        return redirect('/')

    if req.method == "GET":
        return render(req, "user/login.html")
    elif req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']

        # it checks username in User 
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(req, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if profile_obj is None:
            messages.success(req, 'Somethig went wrong try again.')
            return redirect('/login')
        
        # it check the user is email verified or not
        else:
            if not profile_obj.is_verified:
                messages.success(req, 'Profile is not verified check your mail.')
                return redirect('/login')

        # it check the username and password 
        user = auth.authenticate(username = username , password = password)
        if user is not None:
            
            # user loged in
            auth.login(req , user)
            messages.success(req , 'user login successfully')
            return redirect('/')
        else:
            messages.info(req , 'invalid cridenctial')

    return render(req , 'user/login.html' )

# register page
def register(request):
    
    if request.user.is_authenticated:
        return redirect('/')


    if request.method == "GET":
        return render(request, "user/register.html")

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

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
            return render(request, "user/login.html")

        except Exception as e:
            print(e)

# it send email to user with token
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

# it check email verification of user 
def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()

        # checking is there is user created there account or not
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            messages.success(request, 'Somethig went wrong please try again.')
            return redirect('/login')
    except Exception as e:
        print(e)
        return redirect('/')

# for logout
def logout(req):
    auth.logout(req)
    return redirect('/')

# forget password
def forget_password(req ):
    
    if req.user.is_authenticated:
        return redirect('/')

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
            auth_token = str(uuid.uuid4())
            profile_obj.auth_token = auth_token
            profile_obj.save()
            send_mail_for_reset_password(email , auth_token)    
            messages.success(req, 'Email send succesfully check your email.')
            return render(req, f"user/check_mail_send.html" , {'email':email})

        except Exception as e:
            print(e)


def send_mail_for_reset_password(email , token):
    subject = 'Your accounts need to reset password'
    message = f'Hi paste the link to reset the password http://127.0.0.1:8000/reset_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def reset_password(req , auth_token):
    
    if req.user.is_authenticated:
        return redirect('/')

    if req.method == "GET":
        return render(req, "user/reset_password.html")

    elif req.method == 'POST':
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(req, 'Password and confirm password are different.')
            return redirect('/forget_password')

        try:
            profile_obj = Profile.objects.filter(auth_token = auth_token).first()
            print(profile_obj)
            if profile_obj:
                username = profile_obj.user.username
                user_obj = User.objects.filter(username = username).first()
                user_obj.set_password(password)
                user_obj.save()
                messages.success(req, 'Your password is changed.')
                print('ues')
                return redirect('/login')
            else:
                print('no')
                messages.success(req, 'Something went wrong please try again.')
                return redirect('/forget_password')
        except Exception as e:
            print(e)
            return redirect('/')


def category(req, pk):

    ser_obj = Services.objects.filter(pk = pk).first()
    if not ser_obj.sub_category:
        return redirect(f'/service/{ser_obj.id}')
    
    cat_obj = Categorys.objects.filter(service = ser_obj.service)
    print(cat_obj)
    return render(req , 'user/category.html' , {"categorys":cat_obj , 'serviceid': ser_obj.id})

        
        
def service(req ,servicepk, categorypk = None):

    ser_obj = Services.objects.filter(pk = servicepk).first()
    if categorypk is None:
        emp_obj = Employee.objects.filter(service = ser_obj.service).all()
        cat = ser_obj.service
    else:
        cat_obj = Categorys.objects.filter(pk = categorypk).first()
        emp_obj = Employee.objects.filter(category = cat_obj.category).all()
        cat = cat_obj.category
    print(emp_obj[0])

    emplist = []
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    address = profile_obj.address
    for emp in emp_obj:
        Disc={"id":emp.id,"name":emp.name,"image":emp.image,"description":emp.description,"cost":emp.cost,"rating":emp.rating, "address":address}
        emplist.append(Disc)

    return render(req , 'user/service.html' , {'emp_present': len(emp_obj) ,'cat': cat,  'employees' : emplist , 'servicepk':servicepk , 'categorypk' : categorypk})


@login_required(login_url='/login')
def addcart(req , emp_pk ,servicepk, categorypk = None):
    user_obj = req.user
    choose_obj = Choose.objects.create(user_id = user_obj.id , emp_id= emp_pk , cart = True , )
    choose_obj.save()
    messages.success(req, 'Your service is added to cart .')
    if categorypk is None:
        return redirect(f'/service/{servicepk}')
    else:
        return redirect(f'/service/{servicepk}/{categorypk}')
        


@login_required(login_url='/login')
def cart(req):
    emplist = []
    user_obj = req.user
    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = True  ).all()
    for emp in choose_obj:
        data=Employee.objects.filter(pk = emp.emp_id).first() 
        user_obj = User.objects.filter(pk = emp.user_id).first()
        profile_obj = Profile.objects.filter(user = user_obj).first()
        address = profile_obj.address
        Disc={"Name":data.name,"Img":data.image,"desc":data.description,"cost":data.cost,"rating":data.rating,"dataID":emp.id , "address":address}
        emplist.append(Disc)
    return render(req , 'user/cart.html' , { 'present': len(emplist) ,  'employees' : emplist , 'user_id' : user_obj.id})


@login_required(login_url='/login')
def order(req , order_pk = None ,  user_pk = None):
    
    user_obj = req.user
    emplist = []
    if user_pk is None:
        if not order_pk is None:
            choose_obj = Choose.objects.filter(pk = order_pk ).first()
            choose_obj.cart = False
            choose_obj.save()
            messages.success(req, 'Your order is succesfully done .')
    else:
        choose_obj = Choose.objects.filter(user_id = user_pk ).all()
        for obj in choose_obj:
            obj.cart = False
            obj.save()
        messages.success(req, 'Your order is succesfully done .')

    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = False ).all()
    for order in choose_obj:
        # emplist.append(Employee.objects.filter(pk = order.emp_id).first())
        data=Employee.objects.filter(pk = order.emp_id).first() 
        user_obj = User.objects.filter(pk = order.user_id).first()
        profile_obj = Profile.objects.filter(user = user_obj).first()
        address = profile_obj.address
        Disc={"id":data.id,"name":data.name,"image":data.image,"description":data.description,"cost":data.cost,"rating":data.rating, "address":address}
        emplist.append(Disc)
    return render(req , 'user/order.html' , {'present': len(emplist) , 'employees' : emplist} )


@login_required(login_url='/login')
def remove(req , order_pk):

    choose_obj = Choose.objects.filter(pk = order_pk ).first()
    if choose_obj is None:
        return redirect('/cart')
    choose_obj.delete()
    messages.success(req, 'Your cart is succesfully deleted .')

    emplist = []
    user_obj = req.user
    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = True  ).all()
    for emp in choose_obj:
        data=Employee.objects.filter(pk = emp.emp_id).first() 
        Disc={"Name":data.name,"Img":data.image,"desc":data.description,"cost":data.cost,"rating":data.rating,"dataID":emp.id}
        emplist.append(Disc)

    return render(req , 'user/cart.html' , {'present': len(emplist) , 'employees' : emplist , 'user_id' : user_obj.id})



#  Add_employee page
@login_required(login_url='/login')
def add_emp(req , servicepk , categorypk = None):

    # get request
    if req.method == "GET":
        return render(req, "user/add_employee.html")

    if req.method == "POST":
        
        cost = req.POST.get('cost')
        description = req.POST.get('description')

        # condition if file is not uploaded
        if len(req.FILES) != 0:
            image = req.FILES['image']
        else:
            messages.success(req, 'please fill your fields')
            return render(req, 'user/add_employee.html')

        if len(cost) == 0 or len(description) == 0:
            messages.success(req, 'please fill your fields')
            return render(req, 'user/add_employee.html')

        user_obj = req.user
        user_id = user_obj.id
        name = user_obj.username
        
        # getting object of service class
        ser_obj = Services.objects.filter(pk = servicepk).first()

        # if there is no category only service
        if categorypk is None:
            
            emp_obj = Employee.objects.create(user_id=user_id , service= ser_obj.service ,name=name,category='None',cost=cost,description=description,image=image)
            emp_obj.save()
            
            # redirect to service.html
            return redirect(f"/service/{servicepk}")

        else:
            cat_obj = Categorys.objects.filter(pk = categorypk).first()
            emp_obj = Employee.objects.create(user_id=user_id,service= ser_obj.service ,name=name,category=cat_obj.category,cost=cost,description=description,image=image)
            emp_obj.save()
            
            # redirect to service.html
            return redirect(f"/service/{servicepk}/{categorypk}")
        

# checkout.html page
def checkout(req , order_pk = None , user_pk = None ):
    cost = 0
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        messages.success(req, 'Somethig went wrong try again.')
        return redirect('/login')


    if req.method == "POST":
        address = req.POST.get('address')
        profile_obj.address = address
        messages.success(req, 'Address succesfully changed.')
        profile_obj.save()


    # if user select individual cart
    if user_pk is None:
        choose_obj = Choose.objects.filter(pk = order_pk ).first()
        emp_obj = Employee.objects.filter(pk = choose_obj.emp_id ).first()
        cost = emp_obj.cost
        return render(req, 'user/checkout.html' , {'cost':cost , 'order_pk':order_pk , 'address': profile_obj.address})

    # if user select order all
    else:
        choose_obj = Choose.objects.filter(user_id = user_pk , cart=True).all()
        for obj in choose_obj:
            # add cost of all the cart 
            emp_obj = Employee.objects.filter(pk = obj.emp_id ).first()
            cost = cost + emp_obj.cost
        return render(req, 'user/checkout.html' , {'cost':cost , 'user_pk':user_pk , 'address': profile_obj.address})


def profile(req):
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        messages.success(req, 'Somethig went wrong try again.')
        return redirect('/login')

    return render(req, 'user/profile.html' , {'profile':profile_obj})