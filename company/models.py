from django.core.exceptions import ValidationError
from django.db import models
from TPO_app.models import CompanyLogin

# Create your models here.
class CompanyInfo(models.Model):
    username = models.CharField(max_length=200, primary_key=True, default='')
    cname = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    application = models.CharField(max_length=10, default='yes')
    date = models.CharField(max_length=100)
    salary = models.CharField(max_length=200)
    brochure = models.FileField(null=True)

    def __str__(self):
        return self.cname

class SelectedInfo(models.Model):
    username = models.CharField(max_length=200, primary_key=True, default='')
    cname = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    salary = models.CharField(max_length=200)
    result = models.FileField(null=True)

    def __str__(self):
        return self.cname


