import json
import urllib

from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from TPO_website import settings
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import StudentInfo, JobInfo, EventInfo, CompanyInfo, CompanyLogin
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request, 'includes/index.html')


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
                        return redirect("/")
                    elif user_type == 'company':
                        name = request.POST['username']
                        email = request.POST['email']
                        password = request.POST['password1']
                        password = make_password(password)
                        li = CompanyLogin(username = name, email = email, password = password)
                        li.save()
                        form.save()
                        messages.success(request, 'You are successfully registered.')
                        return redirect("/")
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
                                return redirect(reverse('company:index'))
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
    return render(request,'includes/company.html')

@login_required(login_url='/login/')
def register_job(request):
    return render(request,'includes/register_job.html')

def register_job_submit(request):
    print("Hello form is submitted")
    print(request.POST['name'])
    print(request.POST['college'])
    print(request.POST['company'])
    print(request.POST['profile'])
    print(request.POST['graduation'])
    print(request.POST['phoneno'])
    name = request.POST['name']
    email = request.POST['email']
    phoneno = request.POST['phoneno']
    college = request.POST['college']
    graduation = request.POST['graduation']
    company = request.POST['company']
    profile = request.POST['profile']

    Job_Info = JobInfo(uname=name, email=email, phoneno=phoneno, college=college, graduation=graduation, company=company, profile=profile)
    Job_Info.save()
    messages.success(request, 'Your Application is successfully sent.')
    return render(request,'includes/register_job.html')

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
def add_company(request):
    return render(request,'includes/add_company.html')


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

def add_company_submit(request):
    print(request.POST['cname'])
    cname = request.POST['cname']
    role = request.POST['role']
    salary = request.POST['salary']
    Company_Info = CompanyInfo(cname=cname,role=role,salary=salary)
    Company_Info.save()
    messages.success(request, 'Your Company is successfully saved.')
    return render(request,'includes/add_company.html')


def Statistics(request):
    return render(request,'includes/Statistics.html')
# def home_supply_submit(request):
#     print("Hello form is submitted")
#     companyname = request.POST["companyname"]
#     medicine = request.POST["medicine"]
#     quantity = request.POST["quantity"]
#     Supplier_Info = StudentInfo(medicine=medicine, quantity=quantity, companyname=companyname)
#     Supplier_Info.save()
#     return render(request, "supplier/home_supply.html")