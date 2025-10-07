from django.db import models
# Create your models here.
class JobPost(models.Model):
    employer = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50, choices=(
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Other', 'Other'),
    ))
    job_category = models.CharField(max_length=50 ,default = "other", choices=(
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
    posted_on = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(auto_now=False, auto_now_add=False,default='YYYY-MM-DD')

    def __str__(self):
        return f"{self.job_title} "


class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/', blank=True)
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(null=True,blank=True)
    def __str__(self):
        return f"{self.seeker.name} applied for {self.job.job_title}"


class SavedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'seeker')
    
    def __str__(self):
        return f"{self.seeker.username} saved {self.job.job_title}"
    


class AppliedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'seeker')

    def __str__(self):
        return f"{self.seeker.username} applide for  {self.job.job_title}"
    


class AcceptedApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/', blank=True)
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(null=True,blank=True)
    def __str__(self):
        return f"{self.seeker.name} accepted for {self.job.job_title}"




class RejectedApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    seeker = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/', blank=True)
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(null=True,blank=True)
    def __str__(self):
        return f"{self.seeker.name} rejected for {self.job.job_title}"
