from django.shortcuts import render , redirect
from user.models import Services 

# Create your views here.

# home page
def home(req):
    services = Services.objects.all()
    return render(req, 'user/home.html' , {"services" : services})


