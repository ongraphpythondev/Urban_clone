from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required


# checkout.html page
@login_required(login_url='/login')
def checkout(req , order_pk = None , user_pk = None ):
    cost = 0
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    # it check user login with admin account 
    if profile_obj is None:
        return redirect('/login')


    if req.method == "POST":
        address = req.POST.get('address')

        # if user_pk is not none means user user order all operation other wise user use order individullay
        if user_pk is None:
            
            # checking data
            if not address:
                messages.error(req, "Please enter address")
                return redirect(f"/checkout/{order_pk}")
            elif len(address) < 6:
                messages.error(req, "Please enter proper address")
                return redirect(f"/checkout/{order_pk}")
        else:
            
            if not address:
                messages.error(req, "Please enter address")
                return redirect(f"/checkout/{order_pk}/{user_pk}")
            elif len(address) < 6:
                messages.error(req, "Please enter proper address")
                return redirect(f"/checkout/{order_pk}/{user_pk}")

        profile_obj.address = address
        messages.success(req, 'Address succesfully changed.')
        profile_obj.save()


    # if user_pk is not none means user user order all operation other wise user use order individullay
    if user_pk is None:
        choose_obj = Choose.objects.filter(pk = order_pk ).first()
        # update address
        choose_obj.address = profile_obj.address
        choose_obj.save()
        emp_obj = Employee.objects.filter(pk = choose_obj.emp_id ).first()
        cost = emp_obj.cost
        return render(req, 'user/checkout.html' , {'cost':cost , 'order_pk':order_pk , 'address': profile_obj.address})

    
    else:
        choose_obj = Choose.objects.filter(user_id = user_pk , cart=True).all().order_by("-order_date")
        for obj in choose_obj:
            # update address
            obj.address = profile_obj.address
            obj.save()
            emp_obj = Employee.objects.filter(pk = obj.emp_id ).first()
            # add cost of all the cart 
            cost = cost + emp_obj.cost
        return render(req, 'user/checkout.html' , {'cost':cost , 'user_pk':user_pk , 'address': profile_obj.address})

