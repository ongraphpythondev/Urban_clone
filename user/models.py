from django.contrib.auth.models import User
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
    service = models.CharField(max_length=100 )
    name = models.CharField(max_length=100 )
    category = models.CharField(max_length=100 )
    cost = models.IntegerField(default = 0)
    rating = models.FloatField(default = 0)
    description = models.TextField(default = None)
    image = models.TextField(default = None)

    def __str__(self):
        return self.name

class Choose(models.Model):
    user_id = models.CharField(max_length=100 )
    emp_id = models.CharField(max_length=100 )
    cart = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id