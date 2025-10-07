from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','profile_photo','email','contact','user_type','profession']




class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=25,widget=forms.PasswordInput)




class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = '__all__'
        exclude = ['user',]

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        exclude = ['user',]
class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'
        exclude = ['user',]
        

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['employer',]

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','profile_photo','email','contact','user_type','profession','industry']