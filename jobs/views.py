from django.shortcuts import render, redirect , get_object_or_404 , HttpResponse
from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout

# Create your views here.

class JobPosting(View):
     def get(self,request):
          if request.user.is_authenticated and request.user.user_type =='E':
               
               form = JobPostingForm()
               context={
                    'form':form
               }
               return render(request,'jobs/job_post.html',context)
          else:
              messages.error(request,"Only Employer can post Jobs")
              return redirect('home')
     def post(self,request):
          form = JobPostingForm(request.POST)
          user = request.user
          if form.is_valid():
               job = form.save(commit=False)
               job.employer = user 
               # job.company = 
               print("DEBUG >> User:", user, "ID:", user.id)
               job.save()
               messages.success(request,f"Successfully posted {job.job_title} for {job.salary}")
               return redirect('home')
          else:
               messages.error(request,"Form is Invalid")
               context={
                    'form':form
               }
               return render(request,'jobs/job_post.html',context)  
         

         
         

         
from .models import *

def AllJobs(request):
     jobs = JobPost.objects.all()
     return render(request,'jobs/job_list.html',{'jobs':jobs}) 

def job_details(request,job_id):
     job = get_object_or_404(JobPost, id = job_id)
     return render(request,'jobs/job_details.html',{'job':job})


# class JobApplying(View):
#      def get(self,request,job_id):   
#           if  request.user.is_authenticated and request.user.user_type =='J' :
#                form = JobApplicationForm()
#                context={
#                     'form':form
#                }
#                return render(request,'jobs/apply_for_job.html',context)
#           else:
#               messages.error(request,"Only seekers can apply for jobs")          
#               return redirect('home')
#      def post(self,request,job_id):
#          form = JobApplicationForm(request.POST)
#          if form.is_valid():
#               form.save()
#               return redirect('home')
#          else:
#             context={
#                'form':form
#              }
#             return render(request,'jobs/apply_for_job.html',context)       

from django.db.models import Q
@login_required
def apply(request,job_id):
     if request.user.user_type == 'J':
          if request.method =="GET":
               form = JobApplicationForm()
               job = get_object_or_404(JobPost,id = job_id)
               application = JobApplication.objects.filter((Q(seeker=request.user) & Q(job = job)))
               if len(application)>0:
                    messages.error(request,"You have already applied for this job")
                    return redirect('/')
               else:
                    return render(request,'jobs/apply_for_job.html',{'form':form,'job':job})
          elif request.method == "POST":
               job = get_object_or_404(JobPost,id = job_id)
               form = JobApplicationForm(request.POST, request.FILES)
               if form.is_valid():
                    new_application = form.save(commit=False)
                    new_application.job=job
                    new_application.seeker=request.user
                    new_application.save()
                    messages.success(request,f"Successfully applied for {job.job_title} at {job.company.company_name}")
                    return redirect('home')
               else:
                    print(form.errors)   # 🔹 check console for details
                    messages.error(request, f"Error: {form.errors}")
                    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job})
     else:
          messages.error(request,'Onlu Job Seekers can apply for jobs')
@login_required
def applied_jobs(request):
     jobs = JobApplication.objects.filter(seeker_id = request.user.id)
     context = {
          'jobs':jobs
          }
     return render(request,'jobs/applied_jobs.html',context) 

@login_required
def save_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    saved = SavedJob.objects.filter(seeker=request.user, job=job)
    if not saved:
        SavedJob.objects.create(seeker=request.user, job=job)
    return redirect('saved_jobs')
@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(seeker=request.user)
    return render(request, 'jobs/saved_jobs.html', {'saved': saved})
@login_required
def view_applications(request):
     jobs = JobPost.objects.filter(employer = request.user)
     applications = JobApplication.objects.filter( job__in = jobs)
     context = {
          'applications':applications,
          'jobs':jobs
     }
     return render(request,'jobs/applications.html',context)
@login_required
def application_details(request,app_id):
     application = get_object_or_404(JobApplication,id=app_id)
     return render(request,'jobs/application_details.html',{'application':application})

@login_required
def accept_application(request,app_id):
     application = get_object_or_404(JobApplication,id= app_id)
     app = AcceptedApplication.objects.create(job = application.job,seeker = application.seeker,)
     application.delete()
     messages.success(request,f"{application.seeker}'s application Accepted ")
     return redirect('applications')

@login_required
def reject_application(request,app_id):
     application = get_object_or_404(JobApplication,id= app_id)
     app = RejectedApplication.objects.create(job = application.job,seeker = application.seeker,)
     application.delete()
     messages.success(request,f"{application.seeker}'s application Rejected ")
     return redirect('applications')

@login_required
def accepted_application(request):
     job =JobPost.objects.filter( employer = request.user  )
     applications = AcceptedApplication.objects.filter( job__in = job)
     return render(request,'jobs/accepted_applications.html',{'applications':applications})

@login_required     
def rejected_application(request):
     job =JobPost.objects.filter(employer = request.user )
     applications = RejectedApplication.objects.filter(job__in = job)
     return render(request,'jobs/rejected_applications.html',{'applications':applications})    

@login_required     
def my_jobs(request,id):
     jobs = JobPost.objects.filter(employer_id = id)
     return render(request,'jobs/my_jobs.html',{'jobs':jobs})

@login_required     
def delete_job(request,id):
     job = get_object_or_404(JobPost, id = id)
     job.delete()
     messages.success(request,'Job deleted successfully')
     return redirect('home')

@login_required
def accepted_jobs(request):
     jobs = AcceptedApplication.objects.filter(seeker = request.user)
     return render(request,'jobs/accepted_jobs.html',{'jobs':jobs})
@login_required
def rejected_jobs(request):
     jobs = RejectedApplication.objects.filter(seeker = request.user)
     return render(request,'jobs/rejected_jobs.html',{'jobs':jobs})

def search(request):
      q = request.GET.get('q')
      jobs = JobPost.objects.filter(job_title__icontains = q)
      return render(request,'jobs/job_list.html',{'jobs':jobs})