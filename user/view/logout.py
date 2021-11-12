from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth

# for logout


def logout(req):
    auth.logout(req)
    return redirect('/')