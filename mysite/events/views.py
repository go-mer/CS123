from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404, render
from .models import Organization

from django.views.generic import FormView
from .forms import OrgReqForm, EventForm
from django.contrib.auth import authenticate, login
from django.test import Client
from .tables import OrgTable

def homepage(request):
    return render(request, 'events/homepage.html',)
	
def myorgs(request):
	table = OrgTable(Organization.objects.all())
	return render(request, 'events/myOrgs.html', {'table': table})
	
def OrgReqFormView(request):
    if request.method == 'POST':
        form = OrgReqForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            Short_Name = data.get('Short_Name')
            Full_Name = data.get('Full_Name')
            Description = data.get('Description')
            org = Organization.objects.create(Short_Name=Short_Name, Full_Name=Full_Name, Description=Description)
            return HttpResponseRedirect('/events/homepage') 
    else:
        form = OrgReqForm()
    return render(request, 'events/form.html', {'form': form})
	
def EventFormView(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            Name = data.get('Name')
            Date_Time = data.get('Date_Time')
            Venue = data.get('Venue')
            Description = data.get('Description')
            Org_ID = data.get('Org_ID')
            Eval_Key = data.get('Eval_Key')
            org = Organization.objects.create(Name=Name, Date_Time=Date_Time, Venue=Venue, Description=Description, Org_ID=Org_ID, Eval_Key=Eval_Key)
            return HttpResponseRedirect('/events/homepage') 
    else:
        form = EventForm()
    return render(request, 'events/form.html', {'form': form})