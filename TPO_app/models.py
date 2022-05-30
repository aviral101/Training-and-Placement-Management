from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    uname = models.CharField(max_length=200, default='', primary_key = True)
    email = models.EmailField(max_length=200)
    phoneno = models.CharField(max_length=200)
    fname = models.CharField(max_length=200)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    tenth = models.DecimalField(max_digits=5, decimal_places=2)
    twelth = models.DecimalField(max_digits=5, decimal_places=2)
    colname = models.CharField(max_length=200)
    resume = models.FileField(null=True)

    def __str__(self):
        return self.uname

class CompanyLogin(models.Model):
    username = models.CharField(max_length = 200, default='', primary_key = True)
    email = models.EmailField(max_length=200)
    password = models.CharField(('password'), max_length=128)


class JobInfo(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    cname = models.CharField(max_length=200)

    def __str__(self):
        return self.company
        
class EventInfo(models.Model):
    eventname = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    eventdate = models.CharField(max_length=200)
    
    def __str__(self):
        return self.eventname



