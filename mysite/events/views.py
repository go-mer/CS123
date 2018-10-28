from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Organization

from django.views.generic import FormView
from .forms import OrgReqForm

def index(request):
    return HttpResponse("GOOOMER.")
	
def homepage(request):
	org = Organization.objects.all()[:3]
	context = {
        'org': org,
	}
	return render(request, 'events/homepage.html', context)

def OrgReqFormView(request):
    if request.method == 'POST':
        form = OrgReqForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
    else:
        form = OrgReqForm()
    return render(request, 'events/requestOrg.html', {'form': form})