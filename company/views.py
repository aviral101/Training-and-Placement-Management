import json
import urllib

from django.shortcuts import render,redirect,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from TPO_website import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    # try:
    #     if request.session['userid']:
            return render(request,'index.html')
    #     else:
    #         return render(request,'registration/login.html')
    # except KeyError:
    #     return render(request,'registration/login.html')