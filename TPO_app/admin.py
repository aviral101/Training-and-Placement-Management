from django.contrib import admin
from .models import StudentInfo, JobInfo, EventInfo, CompanyLogin, highlight,stat

# Register your models here.
admin.site.register(StudentInfo)
admin.site.register(JobInfo)
admin.site.register(EventInfo)
admin.site.register(CompanyLogin)
admin.site.register(highlight)
admin.site.register(stat)

