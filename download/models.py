from django.db import models

# Create your models here.

class Member(models.Model):
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    dob = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    ssn = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    


    def __str__(self):
        return self.firstname + " " + self.lastname + self.email + " " + self.dob + " " + self.phone_nuumber + " " + self.address + " " + self.ssn + " " + self.city + " " + self.state + " " + self.password


class Tasks_Celery(models.Model):
    task_id = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    progress = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    finished = models.CharField(max_length=40)
    


    def __str__(self):
        return self.task_id + " " + self.description + self.progress + " " + self.status + " " + self.finished



class Tasks_List(models.Model):
    task_id = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    extra_values = models.CharField(max_length=40)
    
    def __str__(self):
        return self.task_id + " " + self.description + " " + self.extra_values

class Full_Tasks_List(models.Model):
    task_id = models.CharField(max_length=40)
    full_task_id = models.CharField(max_length=40)
    user_inputs = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    
    def __str__(self):
        return self.task_id + " " + self.full_task_id + " " + self.user_inputs + " " + self.status


class Full_Tasks_ID(models.Model):
    task_id = models.CharField(max_length=40)
    # full_task_id = models.CharField(max_length=40)
    # user_inputs = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    
    def __str__(self):
        return self.task_id + " "  + self.status


class Posts(models.Model):
    # task_id = models.CharField(max_length=40)
    task_description = models.CharField(max_length=40)
    cost = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    
    def __str__(self):
        return self.task_description + " " + self.cost + " " + self.status



class Users(models.Model):
    user_id = models.CharField(max_length=40)
    outputs = models.CharField(max_length=40)
    # user_inputs = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    
    def __str__(self):
        return self.user_id + " " + self.outputs +  +  self.status



class All_Tasks(models.Model):
    task_id = models.CharField(max_length=40)
    task_description = models.CharField(max_length=40)
    user_id = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    costs = models.CharField(max_length=40)
    submitted_values = models.CharField(max_length=40)
    
    def __str__(self):
        return self.task_id + " " + self.task_description + " " + self.user_id + " " + self.status + " " + self.costs




from django.contrib.auth.models import User
# from django.db import models
from django.utils import timezone


class Owner(User):
    """Inherited Model definition for Owners"""

    orderList = models.TextField(default="")