from django.core.exceptions import ValidationError
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

class highlight(models.Model):
    visiting = models.CharField(max_length=200)
    highest = models.CharField(max_length=20)
    average = models.CharField(max_length=20)
    placement = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.pk and highlight.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Highlight instance')
        return super(highlight, self).save(*args, **kwargs)


class stat(models.Model):
    year = models.CharField(max_length=20)
    company_visited = models.IntegerField(max_length=20)
    report = models.FileField(null=True)
    highest_package = models.CharField(max_length=20)
    average_package = models.CharField(max_length=20)
    cs_total = models.CharField(max_length=20)
    cs = models.CharField(max_length=20)
    it_total = models.CharField(max_length=20)
    it = models.CharField(max_length=20)
    extc_total = models.CharField(max_length=20)
    extc = models.CharField(max_length=20)


    def save(self,*args,**kwargs):
        if stat.objects.count() > 2:
            return ValidationError('No extra enteries can be added')
        else:
            super(stat,self).save(*args,**kwargs)


