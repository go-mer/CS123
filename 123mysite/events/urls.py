from django.urls import path, include
from . import views
from . import models
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^login/$', views.loginView, name='Login'),
    url(r'^logout/$', views.logoutView, name='Logout'),
    url(r'^register/$', views.registerView, name='Register'),
    path('admin/', admin.site.urls),
    url(r'^homepage/$', views.homepage, name='Homepage'),
    url(r'^orgReq/$', views.OrgReqFormView, name='OrgReq'),
    url(r'^myOrgs/$', views.myOrgs, name='MyOrgs'),
    url(r'^eventSched/$', views.EventFormView, name='EventSched'),
    url(r'^viewEvent/$', views.viewEvent,{'id':5}, name='ViewEvent'),
    url(r'^search/$', views.searchView, name='Search'),
    url(r'^eval/$', views.EvalFormView, name='Eval'),
]