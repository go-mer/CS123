from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
	Org_ID = models.BigAutoField(primary_key=True)
	Short_Name = models.CharField(max_length=20, blank=False)
	Full_Name = models.CharField(max_length=50, blank=False)
	Description = models.TextField()
	Approved = models.BooleanField(default=False)

class Moderator(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=False) 
    Org_ID = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)	

class Subscription(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=False) 
    Org_ID = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)
	
class Event(models.Model):
	Event_ID = models.BigAutoField(primary_key=True)
	Name = models.CharField(max_length=50, blank=False)
	Date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
	Time = models.TimeField(auto_now=False, auto_now_add=False, blank=False)
	Venue = models.CharField(max_length=20, blank=False)
	Description = models.TextField()
	Org_ID = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False)
	Eval_Key = models.CharField(max_length=15, blank=False)
	
class EvalForm(models.Model):
	User = models.ForeignKey(User, on_delete=models.CASCADE, blank=False) 
	Event_ID = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
	Rating = models.IntegerField(default=10)
	Strengths = models.TextField()
	Suggestions = models.TextField()
	Learnings = models.TextField()
	Comments = models.TextField()