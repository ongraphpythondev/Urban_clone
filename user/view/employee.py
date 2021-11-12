from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required
import random


#  Add_employee page
@login_required(login_url='/login')
def add_emp(req , servicepk , categorypk = None):

    if req.user.is_authenticated:
        user_obj = req.user
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if profile_obj is None:
            return redirect('/admin')
    # get request
    if req.method == "GET":
        return render(req, "user/add_employee.html")

    if req.method == "POST":
        
        cost = req.POST.get('cost')
        description = req.POST.get('description')
        address = req.POST.get('address')
        print(address)
        # condition if file is not uploaded
        if len(req.FILES) != 0:
            image = req.FILES['image']
        else:
            messages.error(req, 'Please add image')
            return render(req, 'user/add_employee.html')


        if len(cost) == 0 or len(description) == 0 or len(address) == 0:
            messages.error(req, 'please fill your fields')
            return render(req, 'user/add_employee.html')
        elif len(description) < 10:
            messages.error(req, 'please fill proper description')
            return render(req, 'user/add_employee.html')
        elif len(address) < 5:
            messages.error(req, 'please fill proper address')
            return render(req, 'user/add_employee.html')


        user_obj = req.user
        user_id = user_obj.id
        name = user_obj.username
        
        rating = round(random.uniform(3.0,4.8))
        # getting object of service class
        ser_obj = Services.objects.filter(pk = servicepk).first()

        # if there is no category only service
        if categorypk is None:
            
            emp_obj = Employee.objects.create(user_id=user_id , service= ser_obj.service ,name=name,category='None',cost=cost,rating=rating,description=description,address=address,image=image)
            emp_obj.save()
            
            # redirect to service.html
            return redirect(f"/service/{servicepk}")

        else:
            cat_obj = Categorys.objects.filter(pk = categorypk).first()
            emp_obj = Employee.objects.create(user_id=user_id,service= ser_obj.service ,name=name,category=cat_obj.category,cost=cost,rating=rating,description=description,address=address,image=image)
            emp_obj.save()
            
            # redirect to service.html
            return redirect(f"/service/{servicepk}/{categorypk}")
        