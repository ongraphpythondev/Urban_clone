from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 

def login(req):

    # it check user login with admin account 
    # if req.user.is_authenticated:
    #     user_obj = req.user
    #     profile_obj = Profile.objects.filter(user = user_obj).first()
    #     if profile_obj is None:
    #         auth.logout(req)
    #         messages.error(req, 'Admin cannot use this functionality please login user account.')
    #         return redirect('/')
    #     return redirect('/')

    if req.method == "GET":
        return render(req, "user/login.html")

    elif req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']

        # checking data
        if not username:
            messages.error(req, 'Please fill username.')
            return render(req, "user/login.html")
        elif not password:
            messages.error(req, 'Please fill password.')
            return render(req, "user/login.html")

        # it checks username in User 
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(req, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if profile_obj is None:
            messages.error(req, 'Admin cannot use this functionality please login user account.')
            return redirect('/login')
        
        # it check the user is email verified or not
        else:
            if not profile_obj.is_verified:
                messages.error(req, 'Profile is not verified check your mail.')
                return redirect('/login')

        # it check the username and password 
        user = auth.authenticate(username = username , password = password)
        if user is not None:
            
            # user loged in
            auth.login(req , user)
            messages.success(req , 'user login successfully')
            return redirect('/')
        else:
            messages.error(req , 'invalid cridenctial')

    return render(req , 'user/login.html' )


