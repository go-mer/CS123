from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView
from .models import Organization, Moderator, Subscription, Event, EvalForm
from django_tables2 import RequestConfig
from django.contrib.auth.models import User
from django.views.generic import FormView
from .forms import RegisterForm, OrgReqForm, EventForm, ViewEventForm, Evaluation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.test import Client
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.core import serializers

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
    if request.user.is_authenticated:
        modOrgs = Moderator.objects.filter(User=request.user)
        modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
        mod = modOrg.filter(Approved=True)
        subs = Subscription.objects.filter(User=request.user)
        events = Event.objects.filter(Org_ID__in=subs.values('Org_ID'))
        return render(request,'events/homepage.html',{'moderator':mod,'events':events})
    else:
        return redirect('Login')
	
def searchView(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    subs = Subscription.objects.filter(User=request.user)
    subedOrgs = Organization.objects.filter(Org_ID__in=subs.values('Org_ID'))
    query = request.GET.get('q')
    if query:
        r = Organization.objects.filter(Q(Full_Name__icontains=query) | Q(Short_Name__icontains=query))
        results = r.filter(Approved=True)
    else:
        results = Organization.objects.filter()	
    if request.method == 'POST':
        data = request.POST.copy()
        Sub = data.get('Sub')
        Org = data.get('Org')
        User = request.user
        Org_ID = Organization.objects.get(Org_ID=Org)
        if Sub == "Subscribe":
            Subscript = Subscription.objects.create(User=User, Org_ID=Org_ID)
            return redirect('Homepage')
        elif Sub == "Unsubscribe":
            Subscript = Subscription.objects.get(User=User,Org_ID=Org_ID).delete()
            return redirect('Homepage')		
    return render(request,'events/search.html',{'results':results,'subscribed':subedOrgs,'moderator':mod})
	
def myOrgs(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    subs = Subscription.objects.filter(User=request.user)
    subedOrgs = Organization.objects.filter(Org_ID__in=subs.values('Org_ID'))
    orgs = subedOrgs.filter(Approved=True)
    return render(request,'events/myOrgs.html',{'orgs':orgs,'moderator':mod})
	
def viewEvent(request,id):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    event = Event.objects.get(pk=id)
    org = event.Org_ID.Short_Name
    if request.method == 'POST':
        form = ViewEventForm(request.POST)
        request.session['id'] = id
        return redirect('Eval')
        if form.is_valid():
            data = request.POST.copy()
            evalkey = data.get('Eval_Key')
            if evalkey == event.Eval_Key:
                return redirect('Eval',{'eventPK':id})
            else:
                return viewEvent(request,id)
    else:
        form = ViewEventForm()
    return render(request,'events/viewEvent.html',{'form':form,'event':event,'org':org,'moderator':mod})
	
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
            Moderatr = Moderator.objects.create(User=User, Org_ID=Org)
            return redirect('Homepage')
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
            return redirect('Homepage')
    else:
        form = EventForm()
    return render(request, 'events/scheduleEvent.html',{'form':form,'org':Org,'moderator':mod})
	
def EvalFormView(request):
    modOrgs = Moderator.objects.filter(User=request.user)
    modOrg = Organization.objects.filter(Org_ID__in=modOrgs.values('Org_ID'))
    mod = modOrg.filter(Approved=True)
    eventPK = request.session['id']
    del request.session['id']
    eventObject = Event.objects.get(pk=eventPK)
    event = eventObject.Name
    if request.method == 'POST':
        form = Evaluation(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            Rating = data.get('Rating')
            Strengths = data.get('Strengths')
            Suggestions = data.get('Suggestions')
            Learnings = data.get('Learnings')
            Comments = data.get('Comments')
            User = request.user
            eval = EvalForm.objects.create(Rating=Rating, Strengths=Strengths, Suggestions=Suggestions, Learnings=Learnings, Comments=Comments, User=User, Event_ID=eventObject)
            return redirect('Homepage')
    else:
        form = Evaluation()
    return render(request, 'events/eval.html',{'form':form,'event':event,'moderator':mod})

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="evals.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Rating', 'Strengths', 'Suggestions', 'Learnings', 'Comments'])

    evalForms = EvalForm.objects.all().values_list('User', 'Rating', 'Strengths', 'Suggestions', 'Learnings', 'Comments')
    for evalForm in evalForms:
        writer.writerow(evalForm)
    return response