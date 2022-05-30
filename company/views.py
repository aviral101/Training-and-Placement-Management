import datetime
import json
import urllib

from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import CompanyInfo, SelectedInfo
from TPO_app.models import JobInfo, StudentInfo, CompanyLogin
from TPO_website import settings
from django.contrib import messages
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def companyindex(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            return render(request,'companyindex.html', {'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

def logout(request):
    try:
        del request.session['userid']
        messages.success(request, "You were successfully logged out.")
        return redirect('login')
    except KeyError:
        return redirect('login')

def stats(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            return render(request,'stats.html', {'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

def update_company_details(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            try:
                form = CompanyInfo.objects.get(username=name);
                if form is not None:
                    return render(request, 'update_company_details.html', {'form': form, 'name':name})
                else:
                    return render(request, 'update_company_details.html', {'name':name})
            except ObjectDoesNotExist:
                return render(request, 'update_company_details.html', {'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')


def save_company_details(request):
    try:
        if request.session['userid']:
            username = request.session.get('userid')
            print(username)
            cname = request.POST['cname']
            role = request.POST['role']
            salary = request.POST['salary']
            date = request.POST['date']
            brochure = request.FILES['brochure']
            application = request.POST['application']
            Company_Info = CompanyInfo(username=username, cname=cname, role=role, application=application, date=date, salary=salary, brochure=brochure)
            Company_Info.save()
            messages.success(request, 'Your Details were successfully saved.')
            name = username
            return render(request, 'update_company_details.html',{'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def recieved_applications(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            ap = JobInfo.objects.filter(cname = name).values_list('uname', flat=True)
            l=[]
            for a in ap:
                l.append(StudentInfo.objects.get(uname = a))
            return render(request, 'recieved_applications.html',{'name':name, 'l':l})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')


def upload_result(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            return render(request, 'upload_result.html',{'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

def delete(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            return render(request, 'delete.html',{'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

def confirm_delete(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            password = request.POST['password']
            try:
                v = CompanyLogin.objects.get(username=name)
                b = check_password(password, v.password)
                print(b)
                if b is True:
                    li = CompanyInfo.objects.filter(username=name)
                    li.delete()
                    print('company info deleted')
                    si = SelectedInfo.objects.filter(username=name)
                    si.delete()
                    print('selected info deleted')
                    mi = JobInfo.objects.filter(cname=name)
                    mi.delete()
                    print('Job info deleted')
                    ni = CompanyLogin.objects.filter(username=name)
                    ni.delete()
                    print('Company login deleted')
                    user = User.objects.filter(username=name)
                    user.delete()
                    print('User info deleted')
                    del request.session['userid']
                    messages.success(request, "Account was successfully deleted.")
                    return redirect('login')
                else:
                    messages.warning(request, 'Incorrect Password')
                    return render(request, 'delete.html', {'name': name})
            except ObjectDoesNotExist:
                messages.warning(request, 'Invalid User')
                return redirect('login')
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')


def save_result(request):
    try:
        if request.session['userid']:
            name = request.session.get('userid')
            li = CompanyInfo.objects.get(username=name)
            result = request.FILES['result']
            cname = li.cname
            role = li.role
            salary = li.salary
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            li = SelectedInfo(username=name, result=result, cname=cname, role=role, salary=salary, date=date)
            li.save()
            messages.success(request, "Result was successfully uploaded.")
            return render(request, 'upload_result.html',{'name':name})
        else:
            return redirect('login')
    except KeyError:
        return redirect('login')

