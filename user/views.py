from django.shortcuts import render , redirect
from user.models import Services 


# home page
def home(req):
    services = Services.objects.all()
    return render(req, 'user/home.html' , {"services" : services})


