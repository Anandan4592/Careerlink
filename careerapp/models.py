from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    comp_name=models.CharField(max_length=225)
    about=models.CharField(max_length=22225)
    location=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)

class Jobseeker(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=22225,null=True)
    about=models.CharField(max_length=22225)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class Job(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    hire=models.ForeignKey(Recruiter,on_delete=models.CASCADE,null=True)
    jobname=models.CharField(max_length=22225,null=True)
    qualification=models.CharField(max_length=22225)
    experience=models.CharField(max_length=22225,null=True)
    about_job=models.CharField(max_length=22225,null=True)
    posted_at = models.DateTimeField(auto_now_add=True,null=True)
    cancel = models.BooleanField(default=False)

class Applications(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    hire=models.ForeignKey(Recruiter,on_delete=models.CASCADE,null=True)
    jobname=models.ForeignKey(Job,on_delete=models.CASCADE,null=True)
    seeker=models.ForeignKey(Jobseeker,on_delete=models.CASCADE,null=True)
    applied_at = models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=22225,null=True)
    