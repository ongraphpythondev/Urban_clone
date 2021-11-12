from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def notification(req ):
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    emp_obj = Employee.objects.filter(user_id = user_obj.id).all()
    userlist = []
    for emp in emp_obj:
        order_obj = Choose.objects.filter(emp_id=emp.id , cart = False).all().order_by("-order_date")
        for order in order_obj:

            user_id = order.user_id
            user_obj = User.objects.filter(pk = user_id).first()
            name = user_obj.username

            Disc={"name":name,"cost":emp.cost,"category":emp.category,"service":emp.service,"address":order.address,"status":order.status,"orderid":order.id,"datetime":order.order_date}
            userlist.append(Disc)
    userlist = sorted(userlist, key = lambda i: i['datetime'] , reverse=True)
            

    return render(req , 'user/notification.html' , {"present":len(userlist),"users":userlist})


@login_required(login_url='/login')
def decline(req , order_pk):
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    
    order_obj = Choose.objects.filter(pk=order_pk).first()
    order_obj.status = "Canceled"
    order_obj.save()

    return redirect("/notification")


@login_required(login_url='/login')
def accept(req , order_pk):
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    
    order_obj = Choose.objects.filter(pk=order_pk).first()
    order_obj.status = "Approved"
    order_obj.save()

    return redirect("/notification")