from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def order(req , order_pk = None ,  user_pk = None):
    if req.user.is_authenticated:
        user_obj = req.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')
    

    user_obj = req.user
    emplist = []
    if user_pk is None:
        if not order_pk is None:
            choose_obj = Choose.objects.filter(pk = order_pk ).first()
            choose_obj.cart = False
            choose_obj.order_date = datetime.now()
            choose_obj.save()
            messages.success(req, 'Your order is succesfully done .')
            return redirect('/order')
    else:
        choose_obj = Choose.objects.filter(user_id = user_pk ).all().order_by("-order_date")
        for obj in choose_obj:
            obj.cart = False
            obj.order_date = datetime.now()
            obj.save()
        messages.success(req, 'Your order is succesfully done .')
        return redirect('/order')

    choose_obj = Choose.objects.filter(user_id = user_obj.id , cart = False ).all().order_by("-order_date")
    for order in choose_obj:
        
        data=Employee.objects.filter(pk = order.emp_id).first() 
        user_obj = User.objects.filter(pk = order.user_id).first()
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')

        if data.category == "None":
            work = data.service
        else:
            work = data.category
        Disc={"name":data.name,"image":data.image,"description":data.description,"cost":data.cost,"rating":data.rating,"work":work,"address":data.address,"location":order.address,"status":order.status,"orderid":order.id}
        emplist.append(Disc)
    return render(req , 'user/order.html' , {'present': len(emplist) , 'employees' : emplist } )


# it used in while anyone cancle there order
@login_required(login_url='/login')
def cancel_order(req , order_pk):
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    # it change status in database 
    choose_obj = Choose.objects.filter(pk = order_pk).first()
    choose_obj.status = "Canceled"
    messages.success(req, 'Cancel order succesful.')
    choose_obj.save()

    return redirect('/order')