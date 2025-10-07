from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('post-job/',JobPosting.as_view(),name="post_job"),
    path('list/',views.AllJobs,name="job_list"),
    path('details/<int:job_id>/',views.job_details,name="job_details"),
    path('job-application/<int:job_id>',views.apply,name='job_application'),
    path('applied-jobs',views.applied_jobs,name="applied_jobs"),
    path('save-job/<int:job_id>/', views.save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('applications/',views.view_applications,name="applications"),
    path('application_details/<int:app_id>',views.application_details,name="application_details"),
    path('accept_application/<int:app_id>',views.accept_application,name="accept_application"),
    path('reject_application/<int:app_id>',views.reject_application,name="reject_application"),
    path('accepted-applications',views.accepted_application,name="accepted_applications"),
    path('rejected-applications',views.rejected_application,name="rejected_applications"),
    path('my-jobs/<int:id>/',views.my_jobs,name='my_jobs'),
    path('delete-job/<int:id>',views.delete_job,name="delete_job"),
    path('accepted-jobs/',views.accepted_jobs,name="accepted_jobs"),
    path('rejected-jobs/',views.rejected_jobs,name="rejected_jobs"),
    path('search/',views.search,name="search")
    
]
