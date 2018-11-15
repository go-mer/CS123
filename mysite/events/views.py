from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView
from .models import Organization, Moderator, Subscription, Event
from django_tables2 import RequestConfig
from django.contrib.auth.models import User
from django.views.generic import FormView
from .forms import RegisterForm, OrgReqForm, EventForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.test import Client
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Homepage')
    else:
        form = AuthenticationForm()
    return render(request,'events/login.html',{'form':form})

def logoutView(request):
    logout(request)
    return redirect('Login')
	
def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            username = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password1')
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            login(request, user)
            return redirect('Homepage')
    else:
        form = RegisterForm()
    return render(request,'events/register.html',{'form':form})
	
def homepage(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    return render(request,'events/homepage.html',{'moderator':mod})
	
def searchView(request):
    subs = Subscription.objects.filter(User=request.user)
    subedOrgs = Organization.objects.filter(Org_ID__in=subs.values('Org_ID'))
    query = request.GET.get('q')
    if query:
        results = Organization.objects.filter(Q(Full_Name__icontains=query) | Q(Short_Name__icontains=query))
    else:
        results = Organization.objects.filter()
    return render(request,'events/search.html',{'results':results, 'subscribed':subedOrgs})

def myOrgs(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    subs = Subscription.objects.filter(User=request.user)
    subedOrgs = Organization.objects.filter(Org_ID__in=subs.values('Org_ID'))
    orgs = subedOrgs.filter(Approved=True)
    return render(request,'events/myOrgs.html',{'orgs':orgs,'moderator':mod})
	
def viewEvent(request):
    evalCode = request.Get.get('evalCode')
    id = 1
    event = Event.objects.filter(Event_ID=id)
    if evalCode == event[1].get('Eval_Key'):
        
    return render(request,'events/viewEvent.html',{'event':event})
	
def OrgReqFormView(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    if request.method == 'POST':
        form = OrgReqForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            Short_Name = data.get('Short_Name')
            Full_Name = data.get('Full_Name')
            Description = data.get('Description')
            User = request.user
            Org = Organization.objects.create(Short_Name=Short_Name, Full_Name=Full_Name, Description=Description)
            Mod = Moderator.objects.create(User=User, Org_ID=Org)
            return HttpResponseRedirect('/events/homepage')
    else:
        form = OrgReqForm()
    return render(request, 'events/requestOrg.html',{'form':form,'moderator':mod})

def EventFormView(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    Moderate = Moderator.objects.get(User=request.user)
    Org_ID = Moderate.Org_ID
    Org = Org_ID.Short_Name
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            Name = data.get('Name')
            Date = data.get('Date')
            Time = data.get('Time')
            Venue = data.get('Venue')
            Description = data.get('Description')
            Eval_Key = data.get('Eval_Key')
            event = Event.objects.create(Name=Name, Date=Date, Time=Time, Venue=Venue, Description=Description, Org_ID=Org_ID, Eval_Key=Eval_Key)
            return HttpResponseRedirect('/events/homepage') 
    else:
        form = EventForm()
    return render(request, 'events/scheduleEvent.html',{'form':form,'org':Org,'moderator':mod})