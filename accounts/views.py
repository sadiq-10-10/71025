from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import RegisterForm,LoginForm,EducationForm,ExperienceForm,SkillsForm,CompanyForm,UpdateForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import update_session_auth_hash
# Create your views here.

class Register(View):
    def get(self,request):
        form = RegisterForm()
        context = {
            'form':form
        }
        return render(request,'accounts/register.html',context)
    
    def post(self,request):
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request,user)
            
            messages.success(request,f"Account Created successfully, Now you can add other informations ")
            return redirect('education')
           
        else:
            context = {'form': form}
            messages.error(request,"Form is Not Valid")
            return render(request,'accounts/register.html',context) 
    

    
class Login(View):
    def get(self,request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request,'accounts/login.html',context)
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username = username, password = password)
            if user:
                login(request,user)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                context = {
                'form':form
                }
                messages.error(request,"Invalid Credentials")
                return render(request,'accounts/login.html',context)
        else:
            context = {
                'form':form
                }
            messages.error(request,"Form is Not Valid")
            return render(request,'accounts/login.html',context)



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('/')
    
    def post(self,request):
        logout(request)
        return redirect('/')
    

@login_required
def education(request):
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()

            action = request.POST.get("action")
            if action == "add_more":
                messages.success(request, "Education added. You can add another.")
                return redirect("education")   
            else:
                messages.success(request, "Education added successfully")
                return redirect("experience")  
    else:
        form = EducationForm()

    return render(request, "accounts/add_education.html", {"form": form})

@login_required
def experience(request):
    if request.method == "GET":
        form = ExperienceForm()
        return render(request,'accounts/add_experience.html',{'form':form})
    else:
        form = ExperienceForm(request.POST)
        if form.is_valid:
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save() 
            action = request.POST.get("action")
            if action == "add_more":
                messages.success(request, "Education added. You can add another.")
                return redirect("experience")   
            else:
                messages.success(request,'Added your information successfully')
                return redirect('skills')
        else:
            messages.error(request,'Form is Invalid')
            return render(request,'accounts/add_experience.html',{'form':form})
     
@login_required
def skills(request):
    if request.method == "GET":
        form = SkillsForm()
        return render(request,'accounts/add_skills.html',{'form':form})
    else:
        form = SkillsForm(request.POST)
        if form.is_valid():
            skill = form.save(commit = False)
            skill.user = request.user
            skill.save()
            action = request.POST.get("action")
            if action == "add_more":
                messages.success(request, "Education added. You can add another.")
                return redirect("skills")   
            else:
                messages.success(request,'Added your information successfully')
                if request.user.user_type =='J':
                    return redirect('home')
                else:
                    return redirect('company_details')
        else:
            messages.error(request,'Form is Invalid')
            return render(request,'accounts/add_skills.html',{'form':form})
@login_required
def company_details(request):
    if request.method =="GET":
        form = CompanyForm()
        return render(request,'accounts/company_details.html',{'form':form})
    else:
        form = CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.employer = request.user
            company.save()
            messages.success(request,'Company details added successfully')
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request,'Form is Invalid')
        
            return render(request,'accounts/company_details.html',{'form':form})
        


def profile(request,id):
    user = get_object_or_404(User, id = id )
    experience = Experience.objects.filter(user_id=id)
    education = Education.objects.filter(user_id=id)
    skills = Skills.objects.filter(user_id=id)
    company = Company.objects.filter(employer_id = id)
    context = {
        'user':user,
        'education':education,
        'experience':experience,
        'skills':skills,
        'company':company,
    }
    return render(request,'accounts/profile.html',context)


@login_required
def update_profile(request,id):
    user = get_object_or_404(User, id=id)
    if request.user != user:
        messages.error(request,'You cant update another  user profile')
        return redirect("home")

    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile", id=user.id) 
    else:
        form = UpdateForm(instance=user)
        

    return render(request, "accounts/update_profile.html", {"form": form})