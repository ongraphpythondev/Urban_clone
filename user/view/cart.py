from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def addcart(req , emp_pk ,servicepk, categorypk = None):

    # it check user login with admin account 
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    address = profile_obj.address
    # it store on choose table
    choose_obj = Choose.objects.create(user_id = user_obj.id , emp_id= emp_pk , cart = True , address=address)
    choose_obj.save()
    messages.success(req, 'Your service is added to cart .')

    # if there is only service it redirect to service id and if there is category as well it redirect to else part
    if categorypk is None:
        return redirect(f'/service/{servicepk}')
    else:
        return redirect(f'/service/{servicepk}/{categorypk}')
        


@login_required(login_url='/login')
def cart(req):

    # it check user login with admin account 
    if req.user.is_authenticated:
        user_obj = req.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')

    emplist = []
    user_obj = req.user

    #it take all objects of from choose table which has same user_id 
    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = True  ).all().order_by("-order_date")
    for emp in choose_obj:
        
        data=Employee.objects.filter(pk = emp.emp_id).first() 
        user_obj = User.objects.filter(pk = emp.user_id).first()
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')

        # this is if employee has no category
        if data.category == "None":
            work = data.service
        else:
            work = data.category

        # adding all data in dictionary to represent all
        Disc={"name":data.name,"image":data.image,"description":data.description,"cost":data.cost,"rating":data.rating,"work":work,"dataID":emp.id , "address":data.address}
        emplist.append(Disc)
    return render(req , 'user/cart.html' , { 'present': len(emplist) ,  'employees' : emplist , 'user_id' : user_obj.id})


# this is to remove cart
@login_required(login_url='/login')
def remove(req , order_pk):

    # taking unique object 
    choose_obj = Choose.objects.filter(pk = order_pk ).first()
    if choose_obj is None:
        return redirect('/cart')
    choose_obj.delete()
    messages.success(req, 'Your cart is succesfully deleted .')

    emplist = []
    user_obj = req.user

    # taking all object to represent
    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = True  ).all().order_by("-order_date")
    for emp in choose_obj:
        data=Employee.objects.filter(pk = emp.emp_id).first() 

        # adding all to the dictionary
        Disc={"name":data.name,"image":data.image,"description":data.description,"cost":data.cost,"rating":data.rating,"dataID":emp.id , "address":data.address}
        emplist.append(Disc)

    return render(req , 'user/cart.html' , {'present': len(emplist) , 'employees' : emplist , 'user_id' : user_obj.id})

