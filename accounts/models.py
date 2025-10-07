from django.db import models
from django.contrib.auth.models import AbstractUser
from jobs.models import *
class User(AbstractUser):
    name = models.CharField(max_length=70)
    contact = models.CharField(max_length=15)
    user_type = models.CharField(max_length=1,choices = (
        ('E',"Employeer"),
        ('J',"Job-Seeker"),
    ))
    profession = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to='pfps/', height_field=None, width_field=None, max_length=None,null=True,blank=True)
    resume = models.FileField(upload_to='resumes/', max_length=100,null=True,blank=True)
    industry =  models.CharField(max_length=50 , null=True, blank = True, choices=(
        ('healthcare', 'Healthcare & Medical'),
        ('it', 'Information Technology & Software'),
        ('education', 'Education & Training'),
        ('finance', 'Finance & Accounting'),
        ('sales', 'Sales & Marketing'),
        ('engineering', 'Engineering & Manufacturing'),
        ('hospitality', 'Hospitality & Tourism'),
        ('transport', 'Transportation & Logistics'),
        ('legal', 'Legal & Compliance'),
        ('arts', 'Arts, Media & Design'),
        ('other','Other')
        ))
    def __str__(self):
        return self.name    

class Education(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    institute = models.CharField(max_length=50,null=True,blank=True)
    degree = models.CharField(max_length=50,null=True,blank=True)
    passing_year = models.CharField(max_length=10,null=True,blank=True)


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50,null=True,blank=True)
    role = models.CharField(max_length=50,null=True,blank=True)
    job_type = models.CharField(max_length=20,default='other',null=True,blank=True,choices=(
        {'full_time','Full Time'},
        {'part_time','Part Time'},
        {'intern','Internship'},
        {'other','Other'},
        
        
    ))
    duration = models.CharField(max_length=50,null=True,blank=True)

class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField( max_length=20,null=True,blank=True)

class Company(models.Model):
    employer =models.ForeignKey(User,on_delete=models.CASCADE)
    company_logo = models.ImageField(upload_to='logos/', height_field=None, width_field=None, max_length=None,null=True,blank=True)
    company_name = models.CharField(max_length=22,null=True,blank=True)
    company_web = models.URLField(max_length=200,null=True,blank=True)
    company_description = models.TextField(null=True,blank=True)
    company_industry =  models.CharField(max_length=50 , null=True, blank = True, choices=(
        ('healthcare', 'Healthcare & Medical'),
        ('it', 'Information Technology & Software'),
        ('education', 'Education & Training'),
        ('finance', 'Finance & Accounting'),
        ('sales', 'Sales & Marketing'),
        ('engineering', 'Engineering & Manufacturing'),
        ('hospitality', 'Hospitality & Tourism'),
        ('transport', 'Transportation & Logistics'),
        ('legal', 'Legal & Compliance'),
        ('arts', 'Arts, Media & Design'),
        ('other','Other')
        ))
    
    def __str__(self):
        return f'{self.company_name}'
    