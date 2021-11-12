from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required

def category(req, pk):

    # it check user login with admin account 
    if req.user.is_authenticated:
        user_obj = req.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')

    
    ser_obj = Services.objects.filter(pk = pk).first()

    # if any sercice have sub category to redirect to category otherwise service
    if not ser_obj.sub_category:
        return redirect(f'/service/{ser_obj.id}')
    
    cat_obj = Categorys.objects.filter(service = ser_obj.service)

    return render(req , 'user/category.html' , {"categorys":cat_obj , 'serviceid': ser_obj.id})

        
        
def service(req ,servicepk, categorypk = None):

    # it check user login with admin account 
    if req.user.is_authenticated:
        user_obj = req.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/login')

    # it check there is sub category or not
    ser_obj = Services.objects.filter(pk = servicepk).first()
    if categorypk is None:
        emp_obj = Employee.objects.filter(service = ser_obj.service).all()
        cat = ser_obj.service
    else:
        cat_obj = Categorys.objects.filter(pk = categorypk).first()
        emp_obj = Employee.objects.filter(category = cat_obj.category).all()
        cat = cat_obj.category

    emplist = []
    for emp in emp_obj:
        emp_data = Employee.objects.filter(pk = emp.id).first()
        
        # it add all data to list
        emplist.append(emp_data)

    return render(req , 'user/service.html' , {'emp_present': len(emp_obj) ,'cat': cat,  'employees' : emplist , 'servicepk':servicepk , 'categorypk' : categorypk})
