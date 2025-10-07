from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('register/',Register.as_view(),name="register"),
    path('login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
    path('add-education/',views.education,name="education"),
    path('add-experience/',views.experience,name="experience"),
    path('add-skills/',views.skills,name="skills"),
    path('add-company/',views.company_details,name="company_details"),
    path('profile/<int:id>/',views.profile,name = "profile"),
    path('update-profile/<int:id>/',views.update_profile,name="update_profile")
]
