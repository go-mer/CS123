from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin

from events.views import OrgReqFormView

urlpatterns = [
	path('', views.index, name='index'),
	path('homepage/', views.homepage, name='Homepage'),
	path('homepage/OrgReq/', OrgReqFormView, name='OrgReq'),
]