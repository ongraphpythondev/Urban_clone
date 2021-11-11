from django.contrib.auth.models import User
from django.db import models
import time
import os
from uuid import uuid4



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default = None)

    def __str__(self):
        return self.user.username


class Services(models.Model):
    service = models.CharField(max_length=100 )
    sub_category = models.BooleanField(default=False)

    def __str__(self):
        return self.service

class Categorys(models.Model):
    service = models.CharField(max_length=100 )
    category = models.CharField(max_length=100 )

    def __str__(self):
        return self.category


class Employee(models.Model):
    user_id = models.CharField(max_length=100 , default=None)
    service = models.CharField(max_length=100 )
    name = models.CharField(max_length=100 )
    category = models.CharField(max_length=100 , default=None)
    cost = models.IntegerField(default = 0)
    rating = models.FloatField(default = 4.2)
    description = models.TextField(default = None)
    address = models.TextField(blank = True , default = None)
    image = models.FileField(upload_to = 'user/static/user/image')


    def __str__(self):
        return self.name
    



class Choose(models.Model):
    user_id = models.CharField(max_length=100 )
    emp_id = models.CharField(max_length=100 )
    cart = models.BooleanField(default=True)
    address = models.TextField(blank = True , default = None)
    status = models.TextField(blank = True , default = "Not replied")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id