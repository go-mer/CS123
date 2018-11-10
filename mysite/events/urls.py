from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
	path('homepage/', views.homepage, name='Homepage'),
	path('orgReq/', views.OrgReqFormView, name='OrgReq'),
    path('myOrgs/', views.myorgs, name='MyOrgs'),
	path('myOrgs/eventSched/', views.EventFormView, name='EventSched'),
	path('login', views.login, name='Login'),
	path('register', views.register, name='Register'),
]

