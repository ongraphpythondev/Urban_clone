from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from user.models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def profile(req):
    
    # it check user login with admin account 
    user_obj = req.user
    profile_obj = Profile.objects.filter(user = user_obj).first()
    if profile_obj is None:
        return redirect('/login')

    return render(req, 'user/profile.html' , {'profile':profile_obj})
