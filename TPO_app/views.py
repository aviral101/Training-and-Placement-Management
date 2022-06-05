import json
import os
import urllib

from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from company.models import CompanyInfo, SelectedInfo
from TPO_website import settings
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import StudentInfo, JobInfo, EventInfo, CompanyLogin, highlight, stat
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    li = highlight.objects.all()
    return render(request, 'includes/index.html',{'li':li})


@login_required(login_url='/login/')
def update_details(request):
    uname = request.user
    try:
        form = StudentInfo.objects.get(uname = uname);
        if form is not None:
            return render(request, 'includes/update_details.html', {'form': form})
        else:
            return render(request, 'includes/update_details.html')
    except ObjectDoesNotExist:
        return render(request, 'includes/update_details.html')

@login_required(login_url='/login/')
def fill_details(request):
    return render(request, 'includes/fill_details.html')


def register_page(request):
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in.")
        return redirect("/")
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                if result['success']:
                    user_type = request.POST['user_type']
                    if user_type == 'student':
                        print(user_type)
                        form.save()
                        messages.success(request, 'You are successfully registered.')
                        return redirect("login")
                    elif user_type == 'company':
                        name = request.POST['username']
                        email = request.POST['email']
                        password = request.POST['password1']
                        password = make_password(password)
                        li = CompanyLogin(username = name, email = email, password = password)
                        li.save()
                        form.save()
                        messages.success(request, 'You are successfully registered.')
                        return redirect("login")
                else:
                    messages.error(request, "Invalid reCAPTCHA. Please try again.")
                    return redirect("register_page")
        else:
            form = RegisterForm()

        return render(request, "registration/register.html", {"form":form})


def login_request(request):
    if request.user.is_authenticated:
        messages.error(request,"You are already logged in.")
        return redirect("/")
    else:
        if request.method == "POST":
            user_type = request.POST['user_type']
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                print(user_type)
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY, 'response': recaptcha_response }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())

                if result['success']:
                    username = form.cleaned_data.get("username")
                    password = form.cleaned_data.get("password")
                    user_type = request.POST['user_type']
                    if user_type == 'student':
                        user = authenticate(username=username, password=password)
                        if user is not None:
                            login(request, user)
                            try:
                                li = StudentInfo.objects.get(uname=username)
                                if li is not None:
                                    return redirect("/")
                                else:
                                    return redirect('fill_details')
                            except ObjectDoesNotExist:
                                return redirect('fill_details')
                        else:
                            messages.error(request, "Invalid username or password")
                            return redirect("login")
                    elif user_type == 'company':
                        try:
                            v = CompanyLogin.objects.get(username = username)
                            b = check_password(password , v.password)
                            if b is True:
                                request.session['userid'] = username
                                try:
                                    form = CompanyInfo.objects.get(username=username);
                                    if form is not None:
                                        return redirect(reverse('company:companyindex'))
                                    else:
                                        return redirect(reverse('company:update_company_details'))
                                except ObjectDoesNotExist:
                                    return redirect(reverse('company:update_company_details'))
                        except ObjectDoesNotExist:
                            messages.warning(request, 'Incorrect User Id or Password')
                            return redirect('login')
                        return render(request, 'includes/index.html')
                else:
                    messages.error(request,'Invalid reCAPTCHA. Please try again.')
                    return redirect("login")
            else:
                messages.error(request, "Invalid username or password")
                return redirect("login")
        form = AuthenticationForm()
        return render(request, "registration/login.html",{"form": form})



def logout_request(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login/')
def register_student(request):
    return render(request,'TPO_app/register_student.html')

def register_student_submit(request):
    print("Hello form is submitted")
    print(request.POST['name'])
    print(request.POST['event'])
    name = request.POST['name']
    email = request.POST['email']
    phoneno = request.POST['phoneno']
    event = request.POST['event']
    Student_Info = StudentInfo(uname=name,email=email, phoneno=phoneno,event=event)
    Student_Info.save()
    messages.success(request, 'You have successfully registered.')
    return render(request,'TPO_app/register_student.html')



def companies(request):
    cm =CompanyInfo.objects.filter(application='yes')
    jb = JobInfo.objects.filter(uname=request.user).values_list('company', flat=True)
    re = SelectedInfo.objects.all()
    return render(request,'includes/company.html',{'cm':cm, 'jb':jb, 're':re})

@login_required(login_url='/login/')
def register_job(request):
    name = request.user
    cname = request.POST['username']
    c = CompanyInfo.objects.get(username=cname)
    company = c.cname
    Job_Info = JobInfo(uname=name, company=company, cname = cname)
    Job_Info.save()
    messages.success(request, 'Your Application is successfully sent.')
    cm = CompanyInfo.objects.all()
    jb = JobInfo.objects.filter(uname = name).values_list('company', flat=True)
    return render(request, 'includes/company.html', {'cm': cm, 'jb':jb})

def upcoming_events(request):
    return render(request,'includes/upcoming_events.html')


def upcoming_events_submit(request):
    print(request.POST['eventname'])
    eventname = request.POST['eventname']
    description = request.POST['description']
    eventdate = request.POST['eventdate']
    Event_Info = EventInfo(eventname=eventname,description=description, eventdate=eventdate)
    Event_Info.save()
    messages.success(request, 'Your Event is successfully saved.')
    return render(request,'includes/upcoming_events.html')



@login_required(login_url='/login/')
def update_user_details(request):
    if request.method== "POST":
        uname = request.POST['uname']
        email = request.POST['email']
        fname = request.POST['fname']
        colname = request.POST['colname']
        cgpa = request.POST['cgpa']
        tenth = request.POST['tenth']
        twelth = request.POST['twelth']
        phoneno = request.POST['phoneno']
        resume = request.FILES['resume']
        li = StudentInfo(uname = uname, email = email, fname=fname,colname=colname,cgpa=cgpa,tenth=tenth,twelth=twelth, phoneno=phoneno, resume=resume)
        li.save()
        form = StudentInfo()
        messages.success(request, 'Your Details were successfully updated')
        return render(request,'includes/index.html', {'form': form})
    else:
        return render(request,'/')

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def divide(a,b):
   product = (int(a) / int(b))*100
   return(product)

def Statistics(request):
    st = stat.objects.all()
    return render(request,'includes/Statistics.html',{'st':st})
# def home_supply_submit(request):
#     print("Hello form is submitted")
#     companyname = request.POST["companyname"]
#     medicine = request.POST["medicine"]
#     quantity = request.POST["quantity"]
#     Supplier_Info = StudentInfo(medicine=medicine, quantity=quantity, companyname=companyname)
#     Supplier_Info.save()
#     return render(request, "supplier/home_supply.html")